from refunds.models import Refund
from django.utils import timezone
from django.contrib import admin, messages
from django.utils.translation import ngettext as _
from import_export.admin import ImportExportModelAdmin


class RefundAdmin(ImportExportModelAdmin):
	list_display = ['user', 'email', 'name', 'accepted', 'paid', 'date']
	list_filter = ['date', 'accepted', 'paid']
	search_fields = ['user__username', 'name', 'email', 'reason']
	actions = ['accept_request', 'refuse_request']

	date_hierarchy = 'date'

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request):
		return False

	def accept_request(self, request, queryset):
		updated = queryset.update(accepted=True)
		self.message_user(request, _(
				"%d requete acceptée",
				"%d requetes acceptées",
				updated,
			) % updated, messages.SUCCESS)
	accept_request.short_description = 'Accepter les requetes sélectionnées'

 
	def refuse_request(self, request, queryset):
		updated = queryset.update(accepted=False, refused=True, paid=False)
		self.message_user(request, _(
				"%d requete réfusée",
				"%d requetes réfusées",
				updated,
			) % updated, messages.SUCCESS)
	refuse_request.short_description = 'Réfuser les requetes sélectionnées'





admin.site.register(Refund, RefundAdmin)
