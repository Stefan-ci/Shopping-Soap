from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.db.models import Count
from django.views.generic.edit import FormView
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect

import geocoder
import socket

from products.models import Soap, Category
from orders.models import Order, OrderItem
from coupons.models import Coupon
from profils.models import Profile
from newsletter.models import Newsletter
from reports.models import Sales
from refunds.models import Refund
from promotions.models import Promotion
from address.models import ShippingCity, ShippingCountry

from profils.forms import CreateUserForm
from contacts.forms import ContactForm
from coupons.forms import CouponForm
from refunds.forms import RefundForm
from orders.forms import CheckoutForm, OrderConfirmForm

from profils.utils import send_welcome_email, send_suspicious_email
from orders.utils import admin_email_on_order, user_email_on_order
from refunds.utils import user_email_on_refund, admin_email_on_refund

from website.decorators import unauthenticated_user
from website.utils import create_unique_order_code, update_views, get_ip








def home_view(request):
    promotions = Promotion.objects.filter(is_public=True, has_expired=False)[:2]
    popular_items = Soap.objects.filter(is_public=True, is_deleted=False, is_popular=True)
    new_items = Soap.objects.filter(is_public=True, is_deleted=False).order_by('-date')
    
    items = Soap.objects.filter(is_public=True, is_deleted=False).order_by('-id')
    paginator = Paginator(items, 56)
    page = request.GET.get("page")
    items_obj = paginator.get_page(page)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    items_views = Soap.objects.filter(is_deleted=False)
    for item in items_views:
        update_views(request, item)

    # Searching for items/soaps
    if 'soap' in request.GET:
        soap = request.GET['soap']
        return redirect(f'/recherches/?soap={soap}')
    

    context = {
        'items': items_obj,
        'new_items': new_items,
        'promotions': promotions,
        'popular_items': popular_items,
        'current_site': get_current_site(request),
    }

    template_name = 'public/home.html'
    return render(request, template_name, context)









@login_required(login_url='login')
def user_cart_view(request):
    completed_orders = Order.objects.filter(user=request.user, ordered=True)
    try:
        order = Order.objects.get(user=request.user, ordered=False) or None
    except:
        order = None
        messages.warning(request, "Votre panier est vide actuellement")
    context = {
        'order' : order,
        'completed_orders': completed_orders,
        'current_site' : get_current_site(request),
    }
    template_name = 'public/carts/user_cart.html'
    return render(request, template_name, context)





############################################################
"""
	Coupon & Refund Requests views:
		* Add coupon
		* Get registered coupon
        * Refund request
"""
############################################################
def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code) or None
        if coupon.is_active:
            return coupon
        else:
            messages.warning(
                request, f"""
                    Désolé, le coupon avec le code '{coupon.code}' 
                    n'est plus actif.
                """)
            return redirect("checkout")
    except ObjectDoesNotExist:
        messages.warning(request, "Désolé, ce coupon n'existe pas.")
        return redirect("checkout")
    except:
        messages.error(request, """
            Désolé, il semble que ce coupon ait déjà été utilisé. 
            Essayez un autre si vous en avez.
        """)
        return redirect("user-cart")








class AddCouponView(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super(AddCouponView, self).dispatch(request, *args, **kwargs)


    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user,
                    ordered=False
                )

                coupon = Coupon.objects.get(code=code)
                if coupon.is_active:
                    if coupon.user:
                        if self.request.user == coupon.user:
                            order.coupon = get_coupon(self.request, code)
                            order.save()
                            messages.success(
                                self.request, "Coupon ajouté avec succès.")
                            return redirect('checkout')

                        else:  # if not request.user == coupon.user
                            messages.error(
                                self.request, "Ce coupon ne vous ai pas destiné.")
                            return redirect('checkout')
                    else:  # if not coupon.user
                        order.coupon = get_coupon(self.request, code)
                        order.save()
                        messages.success(
                            self.request, "Coupon ajouté avec succès.")
                        return redirect('checkout')

                else:  # if not coupon.is_active
                    messages.success(self.request, """
                        Désolé, ce coupon n'est plus valide.
                    """)
                    return redirect('checkout')

            except ObjectDoesNotExist:
                messages.error(self.request, "Désolé, votre panier est vide")
                return redirect("item-list")






@login_required(login_url='login')
def add_coupon_view(request):
    form = CouponForm
    if request.method == 'POST':
        form = CouponForm(request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=request.user,
                    ordered=False
                )

                coupon = Coupon.objects.get(code=code)
                if coupon.is_active:
                    if coupon.user:
                        if request.user == coupon.user:
                            order.coupon = get_coupon(request, code)
                            order.save()
                            messages.success(
                                request, "Coupon ajouté avec succès.")
                            return redirect('checkout')

                        else:  # if not request.user == coupon.user
                            messages.error(
                                request, "Ce coupon ne vous ai pas destiné.")
                            return redirect('checkout')
                    else:  # if not coupon.user
                        order.coupon = get_coupon(request, code)
                        order.save()
                        messages.success(
                            request, "Coupon ajouté avec succès.")
                        return redirect('checkout')

                else:  # if not coupon.is_active
                    messages.success(request, """
                        Désolé, ce coupon n'est plus valide.
                    """)
                    return redirect('checkout')
            
            except ObjectDoesNotExist:
                messages.warning(request, """
                    Votre panier est vide. Désolé, veuillez sélectionner des 
                    articles et revenez ajouter un coupon.
                """)
                return redirect("item-list")











class RequestRefundView(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super(RequestRefundView, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form,
            'current_site' : get_current_site(self.request),
        }

        template_name = 'public/refunds/request_refund.html'
        return render(self.request, template_name, context)


    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST or None)
        if form.is_valid():
            unique_code = form.cleaned_data.get('unique_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('name')
            
            try:
                order = Order.objects.get(unique_code=unique_code)
                if order:
                    order.refund_requested = True
                    order.save()

                    # Store the refund request
                    refund = Refund.objects.create(
                        user=self.request.user,
                        name=name,
                        order=order,
                        reason=message,
                        accepted=True,
                        email=email,
                        paid=False
                    )

                    try:
                        # Sending emails to admins & user
                        admin_email_on_refund(self.request, refund, order)
                    except:
                        pass

                    try:
                        user_email_on_refund(self.request, refund, order)
                    except:
                        pass
                    messages.info(self.request, """
                        Nous avons reçu votre requête de remboursement. 
                        Elle est en cours de traitement.
                    """)
                    return redirect('item-list')
            except ObjectDoesNotExist:
                messages.error(self.request, """
                    Vous essayez de vous faire rembourser sur un achat qui n'existe pas.
                    Nous ne pouvons donc donner suite à votre requête!
                    Merci et à bientôt.
                """)
                return redirect(self.request.path_info)












############################################################
"""
	Checkout & OrderConfirm Requests views:
		* Checkout
		* Confirm order
"""
############################################################


# Checkout order
@login_required(login_url='login')
def checkout_view(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
    except:
        messages.warning(request, """
                Votre panier est vide. Désolé, veuillez sélectionner des 
                articles et revenez ici.
            """)
        return redirect("user-cart")
    
    form = CheckoutForm
    if request.method == 'POST':
        form = CheckoutForm(request.POST or None)
        
        if not form.is_valid():
            messages.error(request, """
                Le formulaire de vérification n'est pas valide.
                Veuillez vous assurer d'avoir rempli tous les champs 
                nécessaires et avec les informations qu'il faut.
            """)
            return redirect('checkout')
        
        if form.is_valid():
            
            shipping_email = form.cleaned_data.get('email_address')
            shipping_city = form.cleaned_data.get('shipping_city')
            shipping_country = form.cleaned_data.get('shipping_country')
            shipping_firstname = form.cleaned_data.get('first_name')
            shipping_lastname = form.cleaned_data.get('last_name')

            order.shipping_email = shipping_email
            order.shipping_city = shipping_city
            order.shipping_country = shipping_country
            order.shipping_firstname = shipping_firstname
            order.shipping_lastname = shipping_lastname
            
            order.save()

            # if everything is okay, redirect user to confirmation page.
            return redirect('confirm-order')

        else:  # If form is not valid
            form = CheckoutForm()
            messages.error(request, """
                Le formulaire de vérification n'est pas valide.
                Veuillez vous assurer d'avoir rempli tous les champs 
                nécessaires et avec les informations qu'il faut.
            """)
            return redirect('checkout')

    else: # request.method != 'POST'
        form = CheckoutForm()

    context = {
        'form': form,
        'order': order,
    }
    template_name = 'public/orders/checkout_orders.html'
    return render(request, template_name, context)





        


@login_required(login_url='login')
def confirm_order_view(request):
    context = {}
    try:
        order = Order.objects.get(user=request.user, ordered=False)
    except ObjectDoesNotExist:
        messages.warning(request, """
                Votre panier est vide. Désolé, veuillez y ajouter des 
                articles.
            """)
        return redirect("item-list")
    
    if order.shipping_email and order.shipping_city and order.shipping_country:
        context.update({'order': order})
    else:
        messages.warning(request, """
            Votre adresse de livraison est incomplète.
            Veuillez, s'il vous plaît, fournir les informations manquantes 
            en remplissant les champs suivants.
        """)
        return redirect('checkout')
    
    if request.method == 'POST':
        form = OrderConfirmForm(request.POST or None)
        if form.is_valid():
            order_items = order.items.all()
            order_items.update(ordered=True)
            
            now = timezone.now()
            order.ordered = True
            order.shipping_phonenumber = form.cleaned_data.get('phone_number')
            order.unique_code = create_unique_order_code()
            order.ordered_date = now
            order.order_total = order.get_total()
            order.save()

            # Generating QR Code
            order.generate_order_qr_code()
            
            messages.success(request, f"""
                Bravo {request.user.username} votre commande a été enregistreé et
                est en cours de traitement afin de vous livrer le plus 
                tôt possible.
                Merci de nous avoir fait confiance, à bientôt!

                Vous pouvez néanmoins commander d'autres choses encore !
            """)

            user = request.user.profile
            if not user.phone_number:
                user.phone_number = form.cleaned_data.get('phone_number')
                user.save()
            else:
                pass
            
            # Deactivating the current coupon on order if any
            if order.coupon:
                code = order.coupon.code
                coupon = Coupon.objects.get(code=code)
                coupon.is_active = False
                coupon.used = True
                if not coupon.end_date:
                    coupon.end_date = now
                coupon.save()

            # Creating sale object
            Sales.objects.create(
                amount=order.get_total(),
                sale_type="Vente",
                reason=f"Nouvelle commande d'article. Commande:{order.unique_code}",
            )

            # Sending email to admins & user
            try:
                admin_email_on_order(request, order)
                user_email_on_order(request, order)
            except:
                pass
            
            
            return redirect("profile", request.user.profile.unique_token)
            
            
    else:
        messages.warning(request, f"""
            Veuillez remplir correctement le formulaire svp!
        """)
        form = OrderConfirmForm()

    context.update({'form': form})
    
    template_name = 'public/orders/confirm_order.html'
    return render(request, template_name, context)













############################################################
"""
	Items views:
		* List
		* Detail
		* Search
        * Add to cart
        * Remove single item from cart
        * Remove whole item from cart
        * Tags list
"""
############################################################

def item_detail_view(request, slug):
    public_item = Soap.objects.filter(is_public=True, is_deleted=False)
    item = get_object_or_404(public_item, slug=slug)

    # Trying to display simiralities with other items
    item_tags_ids = item.tags.values_list('id', flat=True)
    similar_items = Soap.objects.filter(
        tags__in=item_tags_ids, is_public=True, is_deleted=False
    ).exclude(id=item.id)
    similar_items = similar_items.annotate(same_tags=Count('tags')).order_by('-id')[:6]

    popular_items = Soap.objects.filter(
        is_public=True, is_popular=True, is_deleted=False
    ).exclude(id=item.id).order_by('-id')[:3]

    most_recent_items = Soap.objects.filter(
        is_public=True, is_deleted=False
    ).exclude(id=item.id).order_by('-date')[:5]

    update_views(request, item)

    # Searching for items/soaps
    if 'soap' in request.GET:
        soap = request.GET['soap']
        return redirect(f'/recherches/soaps/?soap={soap}')

    if request.method == 'POST':
        quantity = request.POST['quantity']
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__id=item.id).exists():
                order_item.quantity += int(quantity)
                order_item.save()
                messages.info(
                    request, f"{quantity} {item.name} ajouté(s) à votre panier !")
                return redirect("user-cart")
            else:
                order.items.add(order_item)
                messages.info(
                    request, f"{item.name} ajouté à votre panier !")
                return redirect("user-cart")
        else:
            order = Order.objects.create(user=request.user)
            order.items.add(order_item)
            order_item.quantity += int(quantity)
            order_item.save()
            messages.info(request, f"{quantity} {item.name} ajouté(s) à votre panier !")
    

    # Can't add new order_item with quantity to oder.items.all.
    # I doesn't add item with specified quantity
    # So I try to hide 'form' when certain conditions match the query below.
    try:
        curr_item_order_item = OrderItem.objects.filter(user=request.user, ordered=False, item=item)
        # If there is an order_item based on this item (item in detail view)
        # If item already exists in user choices, show the form else hide it.
    except:
        curr_item_order_item = None
   
    context = {
        'item' : item,
        'popular_items' : popular_items,
        'similar_items' : similar_items,
        'do_not_delete': curr_item_order_item,
        'most_recent_items' : most_recent_items,
        'current_site' : get_current_site(request),
    }
    print()
    template_name = 'public/items/item_detail.html'
    return render(request, template_name, context)












def women_items_list_view(request):
    items_list = Soap.objects.filter(is_public=True, is_deleted=False, type="women").order_by('-id')
    
    paginator = Paginator(items_list, 56)
    page = request.GET.get("page")
    items_obj = paginator.get_page(page)

    try:
        items_list = paginator.page(page)
    except PageNotAnInteger:
        items_list = paginator.page(1)
    except EmptyPage:
        items_list = paginator.page(paginator.num_pages)
    
    # Searching for items/soaps
    if 'soap' in request.GET:
        soap = request.GET['soap']
        return redirect(f'/recherches/?soap={soap}')

    context = {
        'items' : items_obj,
        'current_site' : get_current_site(request),
    }

    for item in items_obj:
        update_views(request, item)
        
    context = {
        'items' : items_obj,
        'current_site' : get_current_site(request),
    }
    template_name = 'public/items/catalogs/women.html'
    return render(request, template_name, context)






def men_items_list_view(request):
    items_list = Soap.objects.filter(is_public=True, is_deleted=False, type="men").order_by('-id')
    
    paginator = Paginator(items_list, 56)
    page = request.GET.get("page")
    items_obj = paginator.get_page(page)

    try:
        items_list = paginator.page(page)
    except PageNotAnInteger:
        items_list = paginator.page(1)
    except EmptyPage:
        items_list = paginator.page(paginator.num_pages)
    
    # Searching for items/soaps
    if 'soap' in request.GET:
        soap = request.GET['soap']
        return redirect(f'/recherches/?soap={soap}')

    context = {
        'items' : items_obj,
        'current_site' : get_current_site(request),
    }

    for item in items_obj:
        update_views(request, item)
        
    context = {}
    template_name = 'public/items/catalogs/men.html'
    return render(request, template_name, context)







def all_items_list_view(request):
    items_list = Soap.objects.filter(is_public=True, is_deleted=False, type="all").order_by('-id')
    
    paginator = Paginator(items_list, 56)
    page = request.GET.get("page")
    items_obj = paginator.get_page(page)

    try:
        items_list = paginator.page(page)
    except PageNotAnInteger:
        items_list = paginator.page(1)
    except EmptyPage:
        items_list = paginator.page(paginator.num_pages)
    
    # Searching for items/soaps
    if 'soap' in request.GET:
        soap = request.GET['soap']
        return redirect(f'/recherches/?soap={soap}')

    context = {
        'items' : items_obj,
        'current_site' : get_current_site(request),
    }

    for item in items_obj:
        update_views(request, item)
        
    context = {}
    template_name = 'public/items/catalogs/all.html'
    return render(request, template_name, context)
        










def children_items_list_view(request):
    items_list = Soap.objects.filter(is_public=True, is_deleted=False, type="children").order_by('-id')
    
    paginator = Paginator(items_list, 56)
    page = request.GET.get("page")
    items_obj = paginator.get_page(page)

    try:
        items_list = paginator.page(page)
    except PageNotAnInteger:
        items_list = paginator.page(1)
    except EmptyPage:
        items_list = paginator.page(paginator.num_pages)
    
    # Searching for items/soaps
    if 'soap' in request.GET:
        soap = request.GET['soap']
        return redirect(f'/recherches/?soap={soap}')

    context = {
        'items' : items_obj,
        'current_site' : get_current_site(request),
    }

    for item in items_obj:
        update_views(request, item)
        
    context = {}
    template_name = 'public/items/catalogs/children.html'
    return render(request, template_name, context)










def items_list_view(request):
    categories = Category.objects.filter(is_public=True)[:20]
    items_list = Soap.objects.filter(is_public=True, is_deleted=False).order_by('-id')

    paginator = Paginator(items_list, 56)
    page = request.GET.get("page")
    items_obj = paginator.get_page(page)

    try:
        items_list = paginator.page(page)
    except PageNotAnInteger:
        items_list = paginator.page(1)
    except EmptyPage:
        items_list = paginator.page(paginator.num_pages)
    
    # Searching for items/soaps
    if 'soap' in request.GET:
        soap = request.GET['soap']
        return redirect(f'/recherches/?soap={soap}')

    context = {
        'items' : items_obj,
        'categories': categories,
        'current_site' : get_current_site(request),
    }

    for item in items_obj:
        update_views(request, item)

    template_name = 'public/items/items_list.html'
    return render(request, template_name, context)












def items_category_list_view(request, category):
    categories = Category.objects.filter(is_public=True)[:20]
    """
        Ensure that entered string/strings can match our query.
        If user entered for example: 'sauce bolivienne', it will turn it on
        'sauce-bolivienne' exact like our slug format that we are querying.
        And if user entered for example: 'sauce, bolivienne, attiéké' (a list)
        it will join all words and return what we want.

        After all that, let's slugify returned objects.
    """
    if type(category) is list:
        category = '-'.join(category)
    else:
        category = str(category).replace(' ', '-')
    
    category = slugify(category, allow_unicode=True)
    
    items = Soap.objects.filter(
        category__slug=category, 
        is_public=True,
        is_deleted=False
    ).order_by('-id')

    paginator = Paginator(items, 56)
    page = request.GET.get("page")
    items_obj = paginator.get_page(page)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    

    # Searching for items/soaps
    if 'soap' in request.GET:
        soap = request.GET['soap']
        return redirect(f'/recherches/?soap={soap}')

    context = {
        'items': items_obj,
        'categories': categories,
        'items_category' : category,
        'current_site' : get_current_site(request)
    }

    template_name = 'public/items/categories_list.html'
    return render(request, template_name, context)












def items_tag_list_view(request, tag):
    # Check item_category_list_view() for explanations.
    if type(tag) is list:
        tag = '-'.join(tag)
    else:
        tag = str(tag).replace(' ', '-')

    tag = slugify(tag, allow_unicode=True)

    items = Soap.objects.filter(
        is_public=True,
        is_deleted=False,
        tags__name=tag
    ).order_by('-id')

    paginator = Paginator(items, 56)
    page = request.GET.get("page")
    items_obj = paginator.get_page(page)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    
    # Searching for items/soaps
    if 'soap' in request.GET:
        soap = request.GET['soap']
        return redirect(f'/recherches/?soap={soap}')


    context = {
        'items': items_obj,
        'items_tag' : tag,
        'current_site' : get_current_site(request)
    }

    template_name = 'public/items/tags_list.html'
    return render(request, template_name, context)










@login_required(login_url='login')
def add_item_to_cart(request, slug):
    public_item = Soap.objects.filter(is_public=True, is_deleted=False)
    item = get_object_or_404(public_item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    # if request.method == 'POST':
    if order_qs.exists():
        order = order_qs[0]
        
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f"{item.name} a encore été ajouté à votre panier !")
            return redirect("item-detail", item.slug)
        else:
            order.items.add(order_item)
            messages.info(request, f"{item.name} a été ajouté à votre panier !")
            return redirect("item-detail", item.slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, 
            ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.info(request, f"{item.name} a été ajouté à votre panier !")
        return redirect("item-detail", item.slug)















@login_required(login_url='login')
def remove_single_item_from_cart(request, slug):
    public_item = Soap.objects.filter(is_public=True, is_deleted=False)
    item = get_object_or_404(public_item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                return redirect("user-cart")
            elif order_item.quantity == 1:
                OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                ).delete()
                return redirect("user-cart")

            else:
                order.items.remove(order_item)
                messages.info(request, f"La quantité de {order_item.item.name} a été modifiée !")
                return redirect("user-cart")
        else:
            messages.error(request, "Cet article ne figure pas dans votre panier ! Ajoutez-le d'abord.")
            return redirect("item-detail", id=id, slug=slug)
    else:
        messages.warning(request, "Votre panier est vide. Désolé, veuillez sélectionner des articles d'abord.")
        return redirect("item-list")








@login_required(login_url='login')
def remove_item_from_cart(request, slug):
    public_item = Soap.objects.filter(is_public=True, is_deleted=False)
    item = get_object_or_404(public_item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, f"{item.name} a été retiré de vos choix !")
            return redirect("user-cart")
        else:
            messages.warning(request, "Cet article ne figure pas dans votre panier ! Ajoutez-le d'abord.")
            return redirect("item-detail", id=id, slug=slug)
    else:
        messages.error(request, "Votre panier est vide !")
        return redirect("item-list")







@login_required(login_url='login')
def add_to_favorites(request, slug):
    public_items = Soap.objects.filter(is_public=True, is_deleted=False)
    item = get_object_or_404(public_items, slug=slug)
    if not item in request.user.profile.favorite_items.all():
        request.user.profile.favorite_items.add(item)
        messages.success(request, f"{item.name} a bien été ajouté à vos favoris")
        return redirect(request.path_info)
    else:
        return redirect("item-detail", item.slug)






@login_required(login_url='login')
def remove_from_favorites(request, slug):
    public_items = Soap.objects.filter(is_public=True, is_deleted=False)
    item = get_object_or_404(public_items, slug=slug)
    if item in request.user.profile.favorite_items.all():
        request.user.profile.favorite_items.remove(item)
        messages.success(request, f"{item.name} a bien été retiré de vos favoris")
        return redirect(request.path_info)
    else:
        return redirect("item-detail", item.slug)





############################################################
"""
	Authentication views:
		* Login
		* Logout
		* Register
"""
############################################################

# User login view


@unauthenticated_user
@csrf_protect
def login_view(request):
    context = {
        'current_site': get_current_site(request),
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user) # Login user for normal login
            Profile.objects.get_or_create(user=user)
            try:
                """
                    Here, I try to update user last info everytime he/she logs in.
                    Data are updated for every POST request on login.
                    Purpose: It can be used to prevent user if suspicious activities 
                    on account.
                """
                profile = request.user.profile
                last_ip = profile.last_login_ip
                old_browser = profile.last_login_browser

                profile.last_login_lat_long = geocoder.ip('me').latlng
                profile.last_login_date = timezone.now()
                profile.last_login_hostname = socket.gethostname()
                profile.last_login_ip = get_ip(request)
                profile.last_login_browser = request.META.get('HTTP_USER_AGENT', '')

                profile.save()

                # Sending email suspicious activities on account.
                send_suspicious_email(request, last_ip, old_browser)
            except:
                pass
            if 'next' in request.POST:
                messages.success(request, "Bienvenue " + str(username) + " !")
                return redirect(request.POST.get('next'))
            
            if user.is_superuser:
                messages.success(request, "Bienvenue " + str(username) + " !")
                return redirect('home')
            return redirect('home')
        else:
            messages.error(request, """
                Erreur de connexion, veuillez recharger la page et réessayer !
            """)
            return redirect('login')
        
    
    
    template_name = 'public/accounts/login.html'
    return render(request, template_name, context)











# User logout view
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, "Vous vous êtes déconnecté avec succès, à bientôt !")
    return redirect('login')












# User register
class RegisterView(FormView):
    template_name = 'public/accounts/register.html'
    form_class = CreateUserForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    @method_decorator(unauthenticated_user)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        
        """
            Create a profile for the new user
        """
        Profile.objects.get_or_create(user=user)
        username = form.cleaned_data.get('username')
        
        try:
            """
                Here, I try to update user last info everytime he/she logs in.
                Data are updated for every POST request on login.
                Purpose: It can be used to prevent user if suspicious activities 
                on account.
            """
            profile = self.request.user.profile

            profile.signup_browser = self.request.META.get('HTTP_USER_AGENT', '')
            profile.signup_ip = get_ip(self.request)
            profile.signup_hostname = socket.gethostname()
            profile.signup_lat_long = geocoder.ip('me').latlng
            
            profile.save()
        except:
            pass

        if user is not None:
            login(self.request, user) # Login the new user
            
            # Sending welcome email.
            try:
                send_welcome_email(self.request)
            except:
                pass
            
        messages.success(self.request, f'Bienvenue {username} !')
        return super(RegisterView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_site': get_current_site(self.request)
        })
        return context









@login_required(login_url='login')
def user_profile_view(request, token):
    completed_orders = Order.objects.filter(user=request.user, ordered=True).order_by('-ordered_date')
    token = request.user.profile.unique_token
    token = token
    context = {
        'completed_orders':completed_orders,
        'current_site': get_current_site(request)
    }
    template_name = 'public/accounts/profile.html'
    return render(request, template_name, context)









@login_required(login_url='login')
def favourites_list_view(request):
    items = request.user.profile.favorite_items.all()
    context = {
        'items': items,
        'current_site': get_current_site(request)
    }
    template_name = 'public/items/favourites.html'
    return render(request, template_name, context)













##################################################################
# Support views:
#   - About
#   - Contact
#   - Support
##################################################################

def about_view(request):
    context = {
        'current_site': get_current_site(request),
    }
    template_name = 'public/support/about.html'
    return render(request, template_name, context)





def support_view(request):
    context = {
        'current_site': get_current_site(request),
    }
    template_name = 'public/support/support.html'
    return render(request, template_name, context)





def contact_view(request):
    contact_form = ContactForm

    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if not contact_form.is_valid():
            messages.warning(request, """
                Veuillez renseigner tous les champs *CORRECTEMENT* svp !
            """)
            return redirect(request.path_info)
        
        if contact_form.is_valid():
            form = contact_form.save(commit=False)
            form.is_answered = False
            form.save()

            name = contact_form.cleaned_data.get('name')
            email = contact_form.cleaned_data.get('email')
            subject = contact_form.cleaned_data.get('subject')
            message = contact_form.cleaned_data.get('message')
            
            
            print(name)
            print(email)
            print(subject)
            print(message)

            # Send emails after contact form submited and saved.
            email_sender = settings.EMAIL_HOST_USER
            try:
                team = get_current_site(request)
                email_receivers = []
                admins = settings.ADMINS
                for admin in admins:
                    email_receivers.append(admin.email)
                
                context = {
                    'team': team,
                    'name': name,
                    'email': email,
                    'subject': subject,
                    'message': message,
                    'email_receivers': email_receivers,
                }

                whole_message = render_to_string('public/emails/contact/admins.html', context)
                email_subject = f"Contact depuis le site {team}"

                send_email = EmailMessage(
                    email_subject,
                    whole_message,
                    email_sender,
                    email_receivers,
                )
                send_email.send(fail_silently=False)


                user_email = [email]
                user_email_subject = f"Votre message sur {team}"
                
                user_context = {
                    'team': team,
                    'name': name,
                    'user_email': user_email
                }

                user_email_message = render_to_string('public/emails/contact/user.html', user_context)
                
                send_user_email = EmailMessage(
                    user_email_subject,
                    user_email_message,
                    email_sender,
                    user_email,
                )
                send_user_email.send(fail_silently=False)
                
                messages.success(request, """
                    Merci de nous avoir contacté, nous vous répondrons sous peu.
                    Merci et à bientôt !
                """)
                return redirect('home')
            except:
                return redirect('home')

    else:
        contact_form = ContactForm()
    context = {
        'contact_form' : contact_form,
        'current_site' : get_current_site(request),
    }

    template_name = 'public/support/contact.html'
    return render(request, template_name, context)










def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('news_email')
        Newsletter.objects.get_or_create(email=email, is_subscribed=True)
        # Send email here.
        messages.success(request, """
            Merci d'avoir souscrit à notre newsletter !
        """)
        return redirect('home')

















##################################################################
# HTMX views:
#   - Cities based on a selected country
##################################################################

def country_cities(request):
    form = CheckoutForm(request.POST)
    print(form['shipping_city'])
    return HttpResponse(form['shipping_city'])




