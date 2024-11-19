from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import PermissionDenied



# Restric the vendor from accessing customer page.
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    if isinstance(context["to_email"], str):
        to_email = []
        to_email.append(context["to_email"])
    else:
        to_email = context["to_email"]
    message = render_to_string(mail_template, context)
    mail = EmailMessage(
        mail_subject,
        message,
        from_email,
        to=to_email
    )
    mail.send()