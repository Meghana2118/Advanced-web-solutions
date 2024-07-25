from django.contrib import admin
from .models import Vendor, UserProfile, Product

admin.site.register([Vendor, UserProfile, Product]) 

