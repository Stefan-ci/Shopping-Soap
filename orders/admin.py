from django.contrib import admin, messages
from django.utils.translation import ngettext
from import_export.admin import ImportExportModelAdmin
from orders.models import Order, OrderItem





class OrderAdmin(ImportExportModelAdmin):
    list_display = ['user', 'unique_code', 'shipping_city', 'shipping_phonenumber',
        'ordered', 'coupon', 'being_delivered', 'received', 'start_date']

    list_filter = ['start_date', 'ordered_date', 'ordered', 
        'being_delivered', 'received', 'refund_requested', 
        'refund_granted']

    search_fields = ['user__username', 'coupon', 'items__item__title', 
        'shipping_phonenumber','shipping_neighborhood', 'shipping_appartment', 
        'shipping_city']

    actions = ['make_refund_accepted', 'mark_as_received', 'mark_as_ordered']

    date_hierarchy = 'ordered_date'

    def has_add_permission(self, request):
        return False

    # def has_delete_permission(self, request, obj=None):
    # 	return False

    # def has_change_permission(self, request, obj=None):
    # 	return False


    def make_refund_accepted(self, request, queryset):
        updated = queryset.update(
            refund_requested=False, 
            refund_granted=True)
        self.message_user(request, ngettext(
                "%d requête de remboursement acceptée",
                "%d requêtes de remboursement acceptée",
                updated,
            ) % updated, messages.SUCCESS)
    text = 'Accepter les requêtes de remboursement'
    make_refund_accepted.short_description = text


    def mark_as_ordered(self, request, queryset):
        updated = queryset.update(
            ordered=True)
        self.message_user(request, ngettext(
                "%d plat commandé avec succès",
                "%d plats commandés avec succès",
                updated,
            ) % updated, messages.SUCCESS)
    text = "Marquer comme 'articles commandés' "
    mark_as_ordered.short_description = text






class OrderItemAdmin(ImportExportModelAdmin):
    list_display = ['user', 'item', 'quantity', 'ordered', 'date']
    list_filter = ['date', 'ordered']
    search_fields = ['item__title', 'quantity', 'user__username']

    date_hierarchy = 'date'

    def has_add_permission(self, request):
        return False

    # def has_delete_permission(self, request, obj=None):
    # 	return False

    # def has_change_permission(self, request, obj=None):
    # 	return True



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
