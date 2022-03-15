import random
import string
import datetime
from django.conf import settings
from coupons.models import Coupon
from django.utils import timezone
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site


sender_email = settings.EMAIL_HOST_USER
one_week = timezone.now() + datetime.timedelta(days=7)
code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
code = str(code) + str(datetime.datetime.today().day)

def send_welcome_email(request):
    coupon = Coupon.objects.create(
        user=request.user,
        code=code,
        reason=f"Inscription de {request.user.username}",
        amount=50,
        is_active=True,
        end_date=one_week,
        used=False
    )

    user_coupon = get_object_or_404(Coupon, id=coupon.id)
    
    team = get_current_site(request)
    receiver_email = [request.user.email]
    subject = f"Bienvenue {request.user.username}"

    context = {
        'team': team,
        'coupon_code': user_coupon.code,
        'username': request.user.username,
        'coupon_amount': user_coupon.amount,
        'coupon_end_date': user_coupon.end_date
    }
    
    message = render_to_string('public/emails/auth/welcome.html', context)
    send_user_email = EmailMessage(
        subject,
        message,
        sender_email,
        receiver_email,
    )
    send_user_email.send(fail_silently=False)
    return



def send_suspicious_email(request, last_ip, old_browser):
    profile = request.user.profile
    
    if profile.last_login_ip is not None and profile.last_login_ip != last_ip:
        team = get_current_site(request)
        context = {
            'team': team,
            'last_ip': last_ip,
            'new_ip': profile.last_login_ip,
            'username': request.user.username,
            'login_date': profile.last_login_date,
            'browser': profile.last_login_browser,
        }
        if profile.last_login_browser is not None and profile.last_login_browser != old_browser:
            context.update({'old_browser': old_browser})

        subject = f"Attention à votre compte {request.user.username}"
        receiver_email = [request.user.email]
        message = render_to_string('public/emails/auth/suspicious.html', context)
        
        send_email = EmailMessage(
            subject,
            message,
            sender_email,
            receiver_email,
        )
        send_email.send(fail_silently=False)
    return

