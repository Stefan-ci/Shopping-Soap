from faqs.models import FAQ
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin



class FAQAdmin(ImportExportModelAdmin):
    prepopulated_fields = {
        'slug': ('question',),
    }
    list_display = ['question', 'answer', 'is_public', 'date']
    list_filter = ['is_public', 'date']
    search_fields = ['question', 'answer']
    date_hierarchy = 'date'


admin.site.register(FAQ, FAQAdmin)
