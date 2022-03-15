from django.contrib import admin
from refunds.models import Refund
from import_export.admin import ImportExportModelAdmin


class RefundAdmin(ImportExportModelAdmin):
	list_display = ['user', 'email', 'name', 'accepted', 'paid', 'reason', 'date']
	list_filter = ['date', 'accepted', 'paid']
	search_fields = ['user__username', 'name', 'email', 'reason']

	date_hierarchy = 'date'

	def has_delete_permission(self, request, obj=None):
		return False
	
	def has_add_permission(self, request):
    		return False

admin.site.register(Refund, RefundAdmin)
