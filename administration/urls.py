from django.urls import path
from administration import views
from administration import default_views as default


urlpatterns = [
    path('', views.admin_home_view, name='admin-home'),

	path('items/table/', views.items_table_view, name='items-table'),
   	path('items/liste/', views.all_items_list_view, name="all-items"),
   	path('items/publics/', views.public_items_list_view, name="public-items"),
	path('item/<int:id>/<str:slug>/', views.item_detail_view, name="admin-item-detail"),



    path('commandes/', views.all_orders_list_view, name='all-orders'),
   	path('commande/<int:id>/<str:unique_code>/', views.order_detail_view, name='order-detail'),
	path('commandes/non-recues/', views.not_received_orders_list_view, name='order-not-received'),
	path('commandes/non-livrees/', views.not_delivered_orders_list_view, name='order-not-delivered'),
	path('commandes/livrees-et-recues/', views.received_orders_list_view, name='order-received'),

   	
	   
	path('inbox/messages/', views.new_messages_list_view, name='messages-inbox'),

	
	
   	# Custom actions (no need templates)
	#path('notifications/supprimer/tout/', default.mark_all_notifs_as_delete, name='mark_all_notifs_as_delete'),
	path('commande/marquer-comme-livree/<int:id>/<str:unique_code>/', default.mark_order_as_delivered, name='mark_order_as_delivered'),
	path('commande/marquer-comme-recue/<int:id>/<str:unique_code>/', default.mark_order_as_received, name='mark_order_as_received'),
	path('commande/imprimer/pdf/<int:id>/<str:unique_code>/', default.render_order_to_pdf_view, name='render_order_to_pdf'),
	path('message/supprimer/<int:id>/', default.mark_contact_as_deleted, name='mark_msg_as_deleted'),
	path('message/marquer-comme-lu/<int:id>/', default.mark_contact_as_read, name='mark_msg_as_read_and_answered'),

   	#path('menu/modifier/<int:id>/', views.update_item_in_table_view, name="update-item-in-table"),
   	path('supprimer/menu/<int:id>/', default.delete_item_view, name='delete-item'),
]


