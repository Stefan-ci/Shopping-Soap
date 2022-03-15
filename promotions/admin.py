from django.contrib import admin
from promotions.models import Promotion
from import_export.admin import ImportExportModelAdmin


class PromotionAdmin(ImportExportModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'added_on', 'has_expired']
    list_filter = ['is_public', 'has_expired', 'added_on', 'start_date', 'end_date']
    search_fileds = ['title', 'description']
    date_hierarchy = 'added_on'
    




admin.site.register(Promotion, PromotionAdmin)



