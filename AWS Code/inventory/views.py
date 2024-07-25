# inventory/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Vendor, Product, Review, UserProfile
from .forms import VendorForm, ProductForm, ReviewForm, UserProfileForm, ContactForm
from .filters import VendorFilter
from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import xlsxwriter
from django.views.decorators.http import require_POST
import logging
logger = logging.getLogger(__name__)

def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = VendorForm(request.POST)
            if form.is_valid():
                vendor = form.save(commit=False)
                vendor.save()
                send_mail('New Vendor Added', f'{vendor.name} has been added to the system.', 'admin@example.com', [request.user.email])
                return redirect('vendor_detail', pk=vendor.pk)
        else:
            form = VendorForm()
        return render(request, 'inventory/index.html', {'form': form})
    else:
        return render(request, 'inventory/index.html')

def about(request):
    return render(request, 'inventory/about.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            recipients = ['admin@example.com']
            send_mail(subject, message, sender, recipients)
            return redirect('index')
    else:
        form = ContactForm()
    return render(request, 'inventory/contact.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def vendor_list(request):
    vendors = Vendor.objects.all()
    filter = VendorFilter(request.GET, queryset=Vendor.objects.all())
    return render(request, 'inventory/vendor_list.html', {'filter': filter})

@login_required
def vendor_detail(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    products = vendor.products.all()
    reviews = vendor.reviews.all()
    return render(request, 'inventory/vendor_detail.html', {'vendor': vendor, 'products': products, 'reviews': reviews})

@permission_required('inventory.add_vendor')
def vendor_new(request):
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.save()
            send_mail('New Vendor Added', f'{vendor.name} has been added to the system.', 'admin@example.com', [request.user.email])
            return redirect('vendor_detail', pk=vendor.pk)
    else:
        form = VendorForm()
    return render(request, 'inventory/vendor_edit.html', {'form': form})

@permission_required('inventory.change_vendor')
def vendor_edit(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == "POST":
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.save()
            send_mail('Vendor Updated', f'{vendor.name} has been updated.', 'admin@example.com', [request.user.email])
            return redirect('vendor_detail', pk=vendor.pk)
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'inventory/vendor_edit.html', {'form': form})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

@login_required
def generate_report(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{vendor.name}_report.pdf"'
    p = canvas.Canvas(response)
    p.drawString(100, 800, f'Vendor Name: {vendor.name}')
    p.drawString(100, 780, f'Website: {vendor.website}')
    p.drawString(100, 760, f'Last Review Date: {vendor.last_review_date}')
    p.drawString(100, 740, f'Description: {vendor.description}')
    p.showPage()
    p.save()
    return response

@login_required
def export_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=vendors.xlsx'
    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    vendors = Vendor.objects.all()
    for vendor in vendors:
        worksheet.write(row, col, vendor.name)
        worksheet.write(row, col + 1, vendor.website)
        worksheet.write(row, col + 2, str(vendor.last_review_date))
        worksheet.write(row, col + 3, vendor.description)
        row += 1
    workbook.close()
    return response

@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            if hasattr(request.user, 'userprofile'):
                product.vendor = request.user.userprofile.vendor
                product.save()
                return redirect('product_list')  # Redirect to product list upon successful creation
        # If form is not valid, or saving fails, log the errors or handle them
        # For now, render the form with errors
    else:
        form = ProductForm()
    return render(request, 'inventory/create_product.html', {'form': form})
