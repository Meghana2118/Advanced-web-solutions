# inventory/forms.py

from django import forms
from .models import Vendor, Product, Review, UserProfile
from django.contrib.auth.models import User

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'website', 'phone_number', 'email', 'last_review_date', 'description']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'documentation', 'image_link', 'vendor']

        
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['vendor'].queryset = Vendor.objects.all()

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['vendor', 'rating', 'comment']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['can_add', 'can_edit', 'can_view']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
