import os
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from django.shortcuts import get_object_or_404, render
from orders.models import Order
from products.models import Soap
from django.contrib.auth.decorators import login_required
import re
import random
import string
from io import BytesIO
from xhtml2pdf import pisa
from html import escape
from django.db.models import Q
from django.template.loader import render_to_string


def update_views(request, object):
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(object)
    hits = hit_count.hits
    hitcontext = context["hitcount"] = {"pk": hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    if hit_count_response.hit_counted:
        hits = hits+1
        hitcontext["hitcounted"] = hit_count_response.hit_counted
        hitcontext["hit_message"] = hit_count_response.hit_message
        hitcontext["total_hits"] = hits




def get_ip(request):
    IP_RE = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    # if neither header contain a value, just use local loopback
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip_address:
        # make sure we have one and only one IP
        try:
            ip_address = IP_RE.match(ip_address)
            if ip_address:
                ip_address = ip_address.group(0)
            else:
                # no IP, probably from some dirty proxy or other device
                # throw in some bogus IP
                ip_address = '10.0.0.1'
        except IndexError:
            pass
    return ip_address





def search_soaps(request):
    items = Soap.objects.filter(is_public=True, is_deleted=False)
    items_count = items.all().count()
    if 'soap' in request.GET:
        soap = request.GET['soap']

        if soap is not None:
            items = items.filter(
                Q(name__contains=soap)|
                Q(description__contains=soap)
            )
            items_count = items.all().count()
            
    
    paginator = Paginator(items, 56)
    page = request.GET.get("page")
    items_obj = paginator.get_page(page)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)


    context = {
        'current_site': get_current_site(request),
        'items': items_obj,
        'items_count': items_count
    }

    template_name = 'public/items/search.html'
    return render(request, template_name, context)






def create_unique_order_code():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=17))
    return code


def is_valid_form(values):
	valid = True
	for field in values:
		if field == '':
			valid = False
	return valid






def fetch_pdf_data(uri, rel):
    path = os.path.join(
        settings.MEDIA_ROOT,
        uri.replace(settings.MEDIA_URL, '')
    )
    return path



@login_required(login_url='login')
def render_order_to_pdf_view(request, unique_code):
    order = get_object_or_404(Order, unique_code=unique_code)
    context = {
        'order': order,
    }
    template = 'public/includes/partials/render_order_to_pdf.html'
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
    
    
    
    