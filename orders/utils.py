from django.conf import settings
from orders.models import Order
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site


sender = settings.EMAIL_HOST_USER


def admin_email_on_order(request, order):
    curr_order = get_object_or_404(Order, id=order.id)
    team = get_current_site(request)
    receivers = []
    admins = dict(settings.ADMINS)
    for admin in admins:
        receivers.append(admins[admin])
    
    context = {
        'team': team,
        'receivers': receivers,
        'curr_order': curr_order,
    }

    subject = f"Nouvelle commande: {curr_order.unique_code}"
    message = render_to_string('public/emails/orders/admins.html', context)

    send_admin_emails = EmailMessage(
        subject,
        message,
        sender,
        receivers,
    )
    send_admin_emails.send(fail_silently=False)
    return





def user_email_on_order(request, order):
    curr_order = get_object_or_404(Order, id=order.id)
    team = get_current_site(request)
    user_email = request.user.email

    context = {
        'team': team,
        'user_email': user_email,
        'curr_order': curr_order,
    }

    subject = f"Nouvelle commande: {curr_order.unique_code}"
    message = render_to_string('public/emails/orders/user.html', context)

    send_user_email = EmailMessage(
        subject,
        message,
        sender,
        [user_email],
    )
    send_user_email.send(fail_silently=False)
    return
