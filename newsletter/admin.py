from re import search
from django.contrib import admin
from newsletter.models import Newsletter
from import_export.admin import ImportExportModelAdmin


class NewsletterAdmin(ImportExportModelAdmin):
    list_display = ['email', 'date', 'is_subscribed', 'is_deleted']
    list_filter = ['date', 'is_subscribed', 'is_deleted']
    search_fields = ['email']

    date_hierarchy = 'date'

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Newsletter, NewsletterAdmin)
