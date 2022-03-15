from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.sites.shortcuts import get_current_site
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from django.shortcuts import render
from products.models import Soap
import hashlib
import json
import re
import random
import string

from django.db.models import Q


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




def generate_user_token(request, username, date_joined):
    hash_string = str(username) + ' ' + str(date_joined)
    hash_encoded = json.dumps(hash_string, sort_keys=True).encode()
    token = hashlib.sha256(hash_encoded).hexdigest()
    return token





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
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
    return code


def is_valid_form(values):
	valid = True
	for field in values:
		if field == '':
			valid = False
	return valid
