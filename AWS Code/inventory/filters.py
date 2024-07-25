# vendor_inventory/inventory/filters.py

import django_filters
from .models import Vendor

class VendorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    website = django_filters.CharFilter(lookup_expr='icontains')
    last_review_date = django_filters.DateFilter()
    # Add additional filters for other fields as needed

    class Meta:
        model = Vendor
        fields = ['name', 'website', 'last_review_date']
