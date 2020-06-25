from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from apps.usuario.models import Usuario

def send_mail(subject, to_email, html_email_template, context):
    """
    Send a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = render_to_string(html_email_template, context)
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')
    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    email_message.attach_alternative(body, 'text/html')

    email_message.send()


def get_list_users(query):
    list_users = []
    for data in query:
        print(data["id"])
        list_users.append(Usuario.objects.get(pk=data["id"]))
    return list_users
