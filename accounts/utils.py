from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import PermissionDenied





# Restrict the custome from accessing vendor page.
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def detectUser(user):
    if user.role == 1:
        redirecturl = "vendor-dashboard"
        return redirecturl
    elif user.role == 2:
        redirecturl = "custDashboard"
        return redirecturl
    elif user.role == None and user.is_superadmin:
        redirecturl = "admin"
        return redirecturl
    


def send_varification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        "user": user,
        "domain": current_site,
        "uid": urlsafe_base64_encode(force_bytes(user.id)),
        "token": default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(
        mail_subject,
        message,
        from_email,
        to=[to_email]
    )
    mail.send()


#? This is the stand alone function for sending email for reset password.

# def send_password_reset_email(request, user):
#     from_email = settings.DEFAULT_FROM_EMAIL
#     current_site = get_current_site(request)
#     mail_subject = "Reset your Password"
#     message = render_to_string("accounts/emails/passwordReset.html", {
#         "user": user,
#         "domain": current_site,
#         "uid": urlsafe_base64_encode(force_bytes(user.id)),
#         "token": default_token_generator.make_token(user),
#     })
#     to_mail = user.email
#     mail = EmailMessage(
#         mail_subject,
#         message,
#         from_email,
#         to=[to_mail]
#     )
#     mail.send()
