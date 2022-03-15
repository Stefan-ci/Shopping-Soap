from django.utils import timezone
from products.models import Soap, Category
from django.contrib import admin, messages
from django.utils.translation import ngettext as _
from import_export.admin import ImportExportModelAdmin


class CategoryAdmin(ImportExportModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }
    list_display = ['name', 'is_public', 'added_on']
    list_filter = ['is_public', 'added_on']
    search_fileds = ['name']

    date_hierarchy = 'added_on'
    

class SoapAdmin(ImportExportModelAdmin):
	list_display = ['name', 'is_public', 'price', 'is_available', 
		'discount_price', 'date', 'category', 'is_popular']
	list_filter = ['is_public', 'is_popular', 'date', 'is_available',
		'delete_date', 'update_date', 'recover_date']

	actions = ['make_not_published', 'make_published', 'is_available',
		'make_popular', 'make_not_popular', 'out_of_stock', 'delete_item',
		'recover_item']
	search_fields = ['name', 'tags__name', 'description', 'price', 
		'discount_price', 'category__name', 'is_available']

	date_hierarchy = 'date'



	def has_delete_permission(self, request, obj=None):
		return False


	"""
		Add custom actions to Model `Item`
	"""
	def make_published(self, request, queryset):
		updated = queryset.update(is_public=True)
		self.message_user(request, _(
				"%d produit marqué comme public",
				"%d produits marqués comme public",
				updated,
			) % updated, messages.SUCCESS)
	make_published.short_description = 'Marquer les produits sélectionnés comme public'



	def make_not_published(self, request, queryset):
		updated = queryset.update(is_public=False)
		self.message_user(request, _(
					"%d produit marqué comme n\'étant pas public",
				"%d produits marqués comme n\'étant pas publics",
				updated,
			) % updated, messages.SUCCESS)
	make_not_published.short_description = 'Marquer les produits sélectionnés comme n\'étant pas publics'



	def make_popular(self, request, queryset):
		updated = queryset.update(is_popular=True)
		self.message_user(request, _(
				"%d produit marqué comme étant populaire",
				"%d produits marqués comme étant populaires",
				updated,
			) % updated, messages.SUCCESS)
	make_popular.short_description = 'Marquer les produits sélectionnés comme étant populaires'



	def make_not_popular(self, request, queryset):
		updated = queryset.update(is_popular=False)
		self.message_user(request, _(
				"%d produit marqué comme n'étant populaires",
				"%d produits marqués comme n'étant populaires",
				updated,
			) % updated, messages.SUCCESS)
	make_not_popular.short_description = 'Marquer les produits sélectionnés comme n\'étant pas populaires'


	def is_available(self, request, queryset):
		updated = queryset.update(is_available='Disponible')
		self.message_user(request, _(
				"%d produit marqué comme étant disponible",
				"%d produits marqués comme étant disponibles",
				updated,
			) % updated, messages.SUCCESS)
	is_available.short_description = 'Marquer les produits sélectionnés comme étant disponibles'



	def out_of_stock(self, request, queryset):
		updated = queryset.update(is_available='En rupture de stock')
		self.message_user(request, _(
				"%d produit marqué comme étant en rupture de stock",
				"%d produits marqués comme étant en rupture de stock",
				updated,
			) % updated, messages.SUCCESS)
	out_of_stock.short_description = 'Marquer les produits sélectionnés comme étant en rupture de stock'


	def delete_item(self, request, queryset):
		updated = queryset.update(
			is_available='deleted',
			is_deleted=True,
			is_public=False,
			is_popular=False,
			delete_date=timezone.now()
		)
		self.message_user(request, _(
				"%d produit supprimé",
				"%d produits supprimés",
				updated,
			) % updated, messages.SUCCESS)
	delete_item.short_description = 'Supprimer les produits sélectionnés'



	def recover_item(self, request, queryset):
		updated = queryset.update(
			is_available='available',
			is_deleted=True,
			is_public=False,
			is_popular=False,
			recover_date=timezone.now()
		)
		self.message_user(request, _(
				"%d produit restauré",
				"%d produits restaurés",
				updated,
			) % updated, messages.SUCCESS)
	recover_item.short_description = 'Restaurer les produits sélectionnés'




admin.site.register(Soap, SoapAdmin)
admin.site.register(Category, CategoryAdmin)



