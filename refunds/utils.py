from django.conf import settings
from orders.models import Order
from refunds.models import Refund
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

sender = settings.EMAIL_HOST_USER


def admin_email_on_refund(request, refund, order):
    curr_req = get_object_or_404(Refund, id=refund.id)
    curr_order = get_object_or_404(Order, id=order.id)

    team = get_current_site(request)
    receivers = []
    admins = dict(settings.ADMINS)
    for admin in admins:
        receivers.append(admins[admin])
    
    context = {
        'team': team,
        'curr_req': curr_req,
        'receivers': receivers,
        'curr_order': curr_order,
    }

    subject = f"Nouvelle requête de remboursement: {curr_order.unique_code}"
    message = render_to_string('public/emails/refunds/admins.html', context)

    send_admin_emails = EmailMessage(
        subject,
        message,
        sender,
        receivers,
    )
    send_admin_emails.send(fail_silently=False)    
    return





def user_email_on_refund(request, refund, order):
    curr_req = get_object_or_404(Refund, id=refund.id)
    curr_order = get_object_or_404(Order, id=order.id)
    team = get_current_site(request)
    user_email = list(curr_req.email)

    context = {
        'team': team,
        'curr_req': curr_req,
        'curr_order': curr_order,
    }

    subject = f"Votre requête de remboursement: {curr_order.unique_code}"
    message = render_to_string('public/emails/refunds/user.html', context)

    send_user_email = EmailMessage(
        subject,
        message,
        sender,
        user_email,
    )
    send_user_email.send(fail_silently=False)
    return
