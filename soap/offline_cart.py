import datetime
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from orders.models import Order, OrderItem
from coupons.forms import CouponForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site




def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = settings.SESSION_COOKIE_AGE
    else:
        max_age = days_expire * 24 * 60 * 60
    dummy = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)
    expires = datetime.datetime.strftime(dummy, "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(
        key, value, max_age=max_age, expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE,
    )







def offline_user_cart(request):
    if request.user.is_authenticated:
        messages.warning(request, "Vous êtes déjà connecté !")
        return redirect('user-cart')
    
    context = {
        'current_site': get_current_site(request),
    }
    
    template_name = 'public/carts/user_offline_cart.html'
    response = render(request, template_name, context)
    response.set_cookie('cart', {})
    
    try:
        cookie_cart = request.COOKIES['cart']
    except KeyError:
        cookie_cart = response.set_cookie('cart', {})
    
    context.update({'cart': cookie_cart})

    return render(request, template_name, context)









@login_required(login_url='login')
def user_cart_view(request):
    form = CouponForm
    completed_orders = Order.objects.filter(user=request.user, ordered=True)
    try:
        order = Order.objects.get(user=request.user, ordered=False) or None
    except:
        order = None
        messages.warning(request, "Votre panier est vide actuellement")
    
            
    context = {
        'form' : form,
        'order' : order,
        'completed_orders': completed_orders,
        'current_site' : get_current_site(request),
    }
    template_name = 'public/carts/user_cart.html'
    return render(request, template_name, context)

