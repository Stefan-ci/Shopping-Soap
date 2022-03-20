from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, View, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, FormView
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.db.models import Q

from products.models import Category, Soap
from coupons.models import Coupon
from contacts.models import Contact
from orders.models import OrderItem, Order
from profils.models import Profile
from reports.models import Sales, Expenses
from refunds.models import Refund

from website.decorators import admin_only, allowed_users
from website.utils import update_views
from administration.utils import generic_data
from coupons.forms import CouponForm




@login_required(login_url='login')
@admin_only
def admin_home_view(request):
    data = generic_data(request)
    recent_orders = Order.objects.filter(
        ordered=True,
        received=False
    ).order_by('-ordered_date')[:20]
    context = {
        'data': data,
        'orders': recent_orders,
    }
    template_name = 'admin/home.html'
    return render(request, template_name, context)






############################################################################
############################################################################
##############                   ITEMS VIEWS             ###################
############################################################################
############################################################################

@login_required(login_url='login')
@admin_only
def item_detail_view(request, id, slug):
    item = get_object_or_404(Soap, id=id)
    slug = item.slug
    slug = slug
    data = generic_data(request)

    context = {
        'data': data,
        'item': item,
    }

    template_name = 'admin/items/item_detail.html'
    return render(request, template_name, context)






@login_required(login_url='login')
@admin_only
def all_items_list_view(request):
    if 'search' in request.GET:
        search_order = request.GET['search']
        items_list = Order.objects.filter(
            name__icontains=search_order,
            is_deleted=False
        ).order_by('-id')[:100]
    else:
        items_list = Soap.objects.filter(
            is_deleted=False
        ).order_by('-id')[:100]

    paginator = Paginator(items_list, 100)
    page = request.GET.get("page")
    items_obj = paginator.get_page(page)

    try:
        items_list = paginator.page(page)
    except PageNotAnInteger:
        items_list = paginator.page(1)
    except EmptyPage:
        items_list = paginator.page(paginator.num_pages)

    data = generic_data(request)

    context = {
        'data': data,
        'items': items_obj,
    }

    template_name = 'admin/items/items_list.html'
    return render(request, template_name, context)









@login_required(login_url='login')
@admin_only
def items_table_view(request):
    categories = Category.objects.filter(is_public=True)
    if 'search' in request.GET:
        search_order = request.GET['search']
        items_list = Soap.objects.filter(
            name__icontains=search_order,
            is_deleted=False
        ).order_by('-id')[:100]
    else:
        items_list = Soap.objects.filter(
            is_deleted=False,
        ).order_by('-id')[:100]

    paginator = Paginator(items_list, 100)
    page = request.GET.get("page")
    items_obj = paginator.get_page(page)

    try:
        items_list = paginator.page(page)
    except PageNotAnInteger:
        items_list = paginator.page(1)
    except EmptyPage:
        items_list = paginator.page(paginator.num_pages)

    data = generic_data(request)

    context = {
        'data': data,
        'items': items_obj,
        'categories': categories,
    }

    template_name = 'admin/items/items_table_list.html'
    return render(request, template_name, context)







@login_required(login_url='login')
@admin_only
def public_items_list_view(request):
    if 'search' in request.GET:
        search_order = request.GET['search']
        items_list = Order.objects.filter(
            is_public=True,
            name__icontains=search_order,
        ).order_by('-id')[:100]
    else:
        items_list = Soap.objects.filter(
            is_public=True,
            is_deleted=False
        ).order_by('-id')[:100]

    paginator = Paginator(items_list, 100)
    page = request.GET.get("page")
    items_obj = paginator.get_page(page)

    try:
        items_list = paginator.page(page)
    except PageNotAnInteger:
        items_list = paginator.page(1)
    except EmptyPage:
        items_list = paginator.page(paginator.num_pages)

    data = generic_data(request)

    context = {
        'data': data,
        'items': items_obj,
    }

    template_name = 'admin/items/public_items.html'
    return render(request, template_name, context)











############################################################################
############################################################################
##############                  ORDERS VIEWS             ###################
############################################################################
############################################################################
@login_required(login_url='login')
@admin_only
def order_detail_view(request, id, unique_code):
    order = get_object_or_404(Order, id=id)
    unique_code = order.unique_code
    unique_code = unique_code

    data = generic_data(request)

    context = {
        'data': data,
        'order': order,
    }

    template_name = 'admin/orders/order_detail.html'
    return render(request, template_name, context)









@login_required(login_url='login')
@admin_only
def all_orders_list_view(request):

    if 'search' in request.GET:
        search_order = request.GET['search']
        orders_list = Order.objects.filter(
            ordered=True,
            unique_code__icontains=search_order,
        ).order_by('-id')[:100]
    else:
        orders_list = Order.objects.filter(
            ordered=True).order_by('-id')[:100]

    paginator = Paginator(orders_list, 100)
    page = request.GET.get("page")
    orders_obj = paginator.get_page(page)

    try:
        orders_list = paginator.page(page)
    except PageNotAnInteger:
        orders_list = paginator.page(1)
    except EmptyPage:
        orders_list = paginator.page(paginator.num_pages)
        
    data = generic_data(request)

    context = {
        'data': data,
        'orders': orders_obj,
    }

    template_name = 'admin/orders/all_orders_list.html'
    return render(request, template_name, context)











@login_required(login_url='login')
@admin_only
def received_orders_list_view(request):

    if 'search' in request.GET:
        search_order = request.GET['search']
        orders_list = Order.objects.filter(
            ordered=True,
            received=True,
            being_delivered=True,
            unique_code__icontains=search_order,
        ).order_by('-id')[:100]
    else:
        orders_list = Order.objects.filter(
            ordered=True,
            received=True,
            being_delivered=True,).order_by('-id')[:100]

    paginator = Paginator(orders_list, 100)
    page = request.GET.get("page")
    orders_obj = paginator.get_page(page)

    try:
        orders_list = paginator.page(page)
    except PageNotAnInteger:
        orders_list = paginator.page(1)
    except EmptyPage:
        orders_list = paginator.page(paginator.num_pages)
        
    data = generic_data(request)

    context = {
        'data': data,
        'orders': orders_obj,
    }

    template_name = 'admin/orders/received_orders.html'
    return render(request, template_name, context)












@login_required(login_url='login')
@admin_only
def not_delivered_orders_list_view(request):

    if 'search' in request.GET:
        search_order = request.GET['search']
        orders_list = Order.objects.filter(
            ordered=True,
            received=False,
            being_delivered=False,
            unique_code__icontains=search_order,
        ).order_by('-id')[:100]
    else:
        orders_list = Order.objects.filter(
            ordered=True,
            received=False,
            being_delivered=False,).order_by('-id')[:100]

    paginator = Paginator(orders_list, 100)
    page = request.GET.get("page")
    orders_obj = paginator.get_page(page)

    try:
        orders_list = paginator.page(page)
    except PageNotAnInteger:
        orders_list = paginator.page(1)
    except EmptyPage:
        orders_list = paginator.page(paginator.num_pages)
        
    data = generic_data(request)

    context = {
        'data': data,
        'orders': orders_obj,
    }

    template_name = 'admin/orders/not_delivered_orders.html'
    return render(request, template_name, context)











@login_required(login_url='login')
@admin_only
def not_received_orders_list_view(request):

    if 'search' in request.GET:
        search_order = request.GET['search']
        orders_list = Order.objects.filter(
            ordered=True,
            received=False,
            being_delivered=True,
            unique_code__icontains=search_order,
        ).order_by('-id')[:100]
    else:
        orders_list = Order.objects.filter(
            ordered=True,
            received=False,
            being_delivered=True
        ).order_by('-id')[:100]

    paginator = Paginator(orders_list, 100)
    page = request.GET.get("page")
    orders_obj = paginator.get_page(page)

    try:
        orders_list = paginator.page(page)
    except PageNotAnInteger:
        orders_list = paginator.page(1)
    except EmptyPage:
        orders_list = paginator.page(paginator.num_pages)

    data = generic_data(request)
    
    context = {
        'data': data,
        'orders': orders_obj,
    }

    template_name = 'admin/orders/not_received_orders.html'
    return render(request, template_name, context)









############################################################################
############################################################################
##############                   INBOX VIEWS             ###################
############################################################################
############################################################################


@login_required(login_url='login')
@allowed_users(allowed_roles=['staffs', 'admins'])
def new_messages_list_view(request):

    if 'search' in request.GET:
        search = request.GET['search']
        unread_contacts_list = Contact.objects.filter(
            unread=True,
            is_answered=False,
            deleted=False,
            name__icontains=search,
        ).order_by('-id')[:100]
    else:
        unread_contacts_list = Contact.objects.filter(
            unread=True,
            is_answered=False,
            deleted=False,).order_by('-id')[:100]

    paginator = Paginator(unread_contacts_list, 100)
    page = request.GET.get("page")
    contacts_obj = paginator.get_page(page)

    try:
        unread_contacts_list = paginator.page(page)
    except PageNotAnInteger:
        unread_contacts_list = paginator.page(1)
    except EmptyPage:
        unread_contacts_list = paginator.page(paginator.num_pages)

    data = generic_data(request)

    context = {
        'data': data,
        'unread_contacts_list': contacts_obj
    }

    template_name = 'admin/inbox/messages_list.html'
    return render(request, template_name, context)











