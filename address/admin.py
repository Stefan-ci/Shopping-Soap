from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from address.models import ShippingCountry, ShippingCity




class ShippingCountryAdmin(ImportExportModelAdmin):
    list_display = ['country', 'date']
    list_filter = ['date']
    search_fields = ['country__name']

    date_hierarchy = 'date'






class ShippingCityAdmin(ImportExportModelAdmin):
    list_display = ['city', 'country', 'date']
    list_filter = ['date']
    search_fields = ['country__name', 'city']

    date_hierarchy = 'date'






admin.site.register(ShippingCity, ShippingCityAdmin)
admin.site.register(ShippingCountry, ShippingCountryAdmin)
