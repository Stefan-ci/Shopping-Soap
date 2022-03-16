from website import views
from django.urls import path
from django.contrib.auth import views as auth_views
from website.utils import search_soaps, render_order_to_pdf_view



urlpatterns = [
    path('', views.home_view, name='home'),
    
    
    # Authentication URLs
    path('connexion/', views.login_view, name='login'),
    path('deconnexion/', views.logout_view, name='logout'),
    path('inscription/', views.RegisterView.as_view(), name='register'),
    path('profile/<str:token>/', views.user_profile_view, name='profile'),
    
    
    
	# Categories URLs
    path('catalogues/tout/', views.all_items_list_view, name='all-items'),
    path('catalogues/femmes/', views.women_items_list_view, name='women-items'),
    path('catalogues/hommes/', views.men_items_list_view, name='men-items'),
    path('catalogues/enfants/', views.children_items_list_view, name='children-items'),
    
    
    
    # Items' URLs
    path('ajouter-aux-favoris/<slug:slug>/', views.add_to_favorites, name='add-to-favorites'),
    path('retirer-des-favoris/<slug:slug>/', views.remove_from_favorites, name='remove-from-favorites'),
    path('ajouter-au-panier/<slug:slug>/', views.add_item_to_cart, name='add-item-to-cart'),
	path('retirer-du-panier/<slug:slug>/', views.remove_item_from_cart, name='remove-from-cart'),
	path('retirer-un-element-du-panier/<slug:slug>/', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
	path('article/<slug>/', views.item_detail_view, name='item-detail'),
   	path('articles/', views.items_list_view, name='item-list'),
	path('articles/categories/categorie=<str:category>/', views.items_category_list_view, name='item-category'),
	path('articles/tags/tag=<str:tag>/', views.items_tag_list_view, name='item-tag'),
   	path('articles/favoris/', views.favourites_list_view, name='favourites'),



	# Checkout URLs
	path('panier/', views.user_cart_view, name='user-cart'),
 	path('verifier/commande/', views.checkout_view, name='checkout'),
   	path('confirmer/commande/', views.confirm_order_view, name='confirm-order'),
	path('ajouter/un-coupon/', views.AddCouponView.as_view(), name='add-coupon'),
	path('requete/remboursement/', views.RequestRefundView.as_view(), name='request-refund'),



	# Support URLs
    path('a-propos/', views.about_view, name='about'),
    path('faqs/', views.faqs_view, name='faqs'),
    path('faqs/<str:slug>/', views.faq_detail_view, name='faq'),
    path('contactez-nous/', views.contact_view, name='contact'),

    
    
    
   	path('recherches/', search_soaps, name='search-items'),
	path('commande/imprimer/pdf/<str:unique_code>/', render_order_to_pdf_view, name='render_order_to_pdf'),
   	path('newsletter/souscrire/', views.subscribe_newsletter, name='subscribe-newsletter'),
    
    
    
    # Password reset URLs
	path('reinitialisation/mot-de-passe/', auth_views.PasswordResetView.as_view(template_name='public/password/forgot_form.html'), name="reset_password"), 
	path('reinitialisation/mot-de-passe/requete-envoye/', auth_views.PasswordResetDoneView.as_view(template_name='public/password/reset_sent.html'), name="password_reset_done"),   
	path('reinitialisation/mot-de-passe/confirmation/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='public/password/reset_form.html'), name="password_reset_confirm"), 
	path('reinitialisation/mot-de-passe/succes/', auth_views.PasswordResetCompleteView.as_view(template_name='public/password/reset_complete.html'), name="password_reset_complete"),
    
]


htmx_urlpatterns = [
	path('cities/', views.country_cities, name="country-cities"),
]


urlpatterns += htmx_urlpatterns

