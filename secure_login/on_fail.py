from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


def email_user(username, password, **kwargs):
    try:
        user = User.objects.get(username=username)
        message = render_to_string("secure_login/failed_login_user.txt")
        send_mail("failed_login", message, settings.DEFAULT_FROM_EMAIL, [user.email])

    except User.DoesNotExist:
        pass
