from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site



sender = settings.EMAIL_HOST_USER


def admin_email_on_contact(request, subject, message, form):
    team = get_current_site(request)
    
    receivers = []
    admins = dict(settings.ADMINS)
    for admin in admins:
        receivers.append(admins[admin])
    
    name = form.cleaned_data.get('name')
    email = form.cleaned_data.get('email')
    subject = form.cleaned_data.get('subject')
    message = form.cleaned_data.get('message')
    
    context = {
        'team': team,
        'name': name,
        'email': email,
        'subject': subject,
        'message': message,
        'email_receivers': receivers,
    }

    email_subject = f"Contact depuis le site: {team}"
    full_message = render_to_string('public/emails/contact/admins.html', context)

    send_admin_emails = EmailMessage(
        email_subject,
        full_message,
        sender,
        receivers,
    )
    send_admin_emails.send(fail_silently=False)
    print(f"\n\n\n{receivers}\n\n\n")
    return





def user_email_on_contact(request, form):
    team = get_current_site(request)
    
    name = form.cleaned_data.get('name')
    email = form.cleaned_data.get('email')
    
    user_email = [email]

    context = {'team': team, 'name': name}

    user_email_subject = f"Votre message sur {team}"
    user_email_message = render_to_string('public/emails/contact/user.html', context)

    send_user_email = EmailMessage(
        user_email_subject,
        user_email_message,
        sender,
        user_email,
    )
    send_user_email.send(fail_silently=False)
    return



