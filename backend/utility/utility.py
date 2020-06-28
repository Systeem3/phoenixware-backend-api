from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import datetime
from apps.usuario.models import Usuario
from apps.proyecto.models import Proyecto


# from rest_framework.renderers import JSONRenderer

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


def get_miembros(data):
    result = []
    for row in data:
        proyecto = Proyecto.objects.get(pk=row["proyecto"])
        usuario = Usuario.objects.get(pk=row["usuario"])
        # empleado = Empleado.objects.filter(usuario=usuario)
        obj = {
            "id": row["id"],
            "rol": row["rol"],
            "proyecto": {
                'id': proyecto.id,
                'nombre': proyecto.nombre,
            },
            "usuario": {
                'id': usuario.id,
                'correo': usuario.email,
                'nombre': usuario.empleado.nombre
            },

        }
        result.append(obj)
    return result


def get_time(fecha_1, fecha_2):
    fecha_1 = datetime.datetime.strptime(fecha_1, '%Y-%m-%d')
    fecha_2 = datetime.datetime.strptime(fecha_2, '%Y-%m-%d')
    time = fecha_2 - fecha_1
    return int(time.days)
