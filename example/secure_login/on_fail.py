from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from .models import FailedLogin

def email_user(username, password, **kwargs):
    try:
        user = User.objects.get(username=username)
        message = render_to_string("secure_login/failed_login_user.txt")
        send_mail("failed_login", message, settings.DEFAULT_FROM_EMAIL, [user.email])

    except User.DoesNotExist:
        pass

def populate_failed_requests(username, password, **kwargs):
    request = kwargs.get("request")
    if request and get_client_ip(request):
        ip = get_client_ip(request)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        FailedLogin.objects.create(user=user, ip=ip)



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = None
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip