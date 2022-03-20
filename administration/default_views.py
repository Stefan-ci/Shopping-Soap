from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, View, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, FormView
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives


from datetime import datetime
import os
from io import BytesIO
from xhtml2pdf import pisa
from html import escape

from products.models import Soap
from coupons.models import Coupon
from contacts.models import Contact
from orders.models import OrderItem, Order
from profils.models import Profile
from reports.models import Sales, Expenses

from website.decorators import admin_only, allowed_users
from website.utils import update_views
from coupons.forms import CouponForm







@login_required(login_url='login')
@admin_only
def mark_order_as_delivered(request, id, unique_code):
    order = get_object_or_404(Order, id=id)
    unique_code = order.unique_code
    unique_code = unique_code
    order.being_delivered = True
    order.save()
    messages.success(request, "Commande marquée comme ayant été livrée !!!")
    _next = request.GET.get('next')
    if _next:
        return redirect(_next)
    return redirect('order-detail', order.id, order.unique_code)





@login_required(login_url='login')
@admin_only
def mark_order_as_received(request, id, unique_code):
    order = get_object_or_404(Order, id=id)
    unique_code = order.unique_code
    unique_code = unique_code
    if order.being_delivered == False:
        messages.error(request, """
            Erreur, la commande n'était en cours de livraison 
            et vous voulez la marquer ayant été reçue par l'utilisateur.
            Il faut que la commande soit livrée avant de pouvoir être 
            marquée comme ayant été reçue par le destinataire !
        """)
        return redirect('order-detail', order.id, order.unique_code)
    else:
        order.being_delivered = True
        order.received = True
        order.save()
        messages.success(request, "Commande marquée comme ayant été reçue !!! Merci.")
        _next = request.GET.get('next')
        if _next:
            return redirect(_next)
        return redirect('order-detail', order.id, order.unique_code)






@login_required(login_url='login')
@admin_only
def mark_contact_as_deleted(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.deleted = True
    contact.save()
    messages.success(request, "Message supprimé !!!")
    _next = request.GET.get('next')
    if _next:
            return redirect(_next)
    return redirect('new-messages')



@login_required(login_url='login')
@admin_only
def mark_contact_as_read(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.unread = False
    contact.is_answered = True
    contact.save()
    messages.success(request, "Message marqué comme non lu")
    _next = request.GET.get('next')
    if _next:
        return redirect(_next)
    return redirect('new-messages')








def fetch_pdf_data(uri, rel):
    path = os.path.join(
        settings.MEDIA_ROOT,
        uri.replace(settings.MEDIA_URL, '')
    )
    return path




@login_required(login_url='login')
@admin_only
def render_order_to_pdf_view(request, id, unique_code):
    order = get_object_or_404(Order, id=id)
    unique_code = order.unique_code
    unique_code = unique_code
    context = {
        'order': order,
    }
    template = 'admin/admin_includes/partials/render_order_to_pdf.html'
    html = render_to_string(template, context=context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), dest=result, link_callback=fetch_pdf_data)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("""
        Erreur de chargement du document PDF
        <pre>
            %s
        </pre>
    """ % escape(html))





@login_required(login_url='login')
@admin_only
def delete_item_view(request, id):
    item = get_object_or_404(Soap, id=id)
    item.is_deleted = True
    item.is_public = False
    item.is_popular = False
    item.delete_date = timezone.now()
    item.is_available = 'Supprimé'
    item.save()
    return redirect('items-table')

