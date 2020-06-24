from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('tipo_usuario', "1")

        if extra_fields.get('tipo_usuario') is None:
            raise ValueError(_('Superuser must have type_user=1.'))
        return self.create_user(email, password, **extra_fields)

    def generate_password(self, name: str, last_name: str) -> str:
        """
        :param name:
        :param last_name:
        :return: password generado de la siguiente forma:
        EG-> nombre: Neptalí Piña , password generado:NAPhoenix7*
        """
        name_first_capital_letter = name[0].upper()
        last_name_last_capital_letter = last_name[len(last_name) - 1].upper()
        name_length = str(len(name))
        password = name_first_capital_letter + last_name_last_capital_letter + "Phoenix" + name_length + "*"
        return password



