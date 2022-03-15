from django.contrib import admin
from coupons.models import Coupon
from import_export.admin import ImportExportModelAdmin



class CouponAdmin(ImportExportModelAdmin):
    list_display = ['user', 'code', 'amount', 'end_date', 'is_active', 'used', 
        'date']
    list_filter = ['end_date', 'is_active', 'date', 'used']
    search_fields = ['code', 'amount']
    date_hierarchy = 'date'


admin.site.register(Coupon, CouponAdmin)
