from django.contrib.auth import backends
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string

DEFAULT_CHECKERS = ["secure_login.checkers.no_weak_passwords",
                    "secure_login.checkers.no_short_passwords",
                    "secure_login.checkers.no_username_password_same"]

checkers = getattr(settings, "SECURE_LOGIN_CHECKERS", DEFAULT_CHECKERS)

def get_callable(callable_str):
    path = callable_str.split(".")
    module_name = ".".join(path[:-1])
    callable_name = path[-1]
    module = __import__(module_name, {}, {}, [callable_name])
    callable_ = getattr(module, callable_name)
    return callable_


class SecureLoginBackend(backends.ModelBackend):

    def __init__(self, *args, **kwargs):
        super(SecureLoginBackend, self).__init__(*args, **kwargs)


    def authenticate(self, username=None, password=None, **kwargs):
        for checker in checkers:
            if not get_callable(checker)(username, password, **kwargs):
                return None
        user = super(SecureLoginBackend, self).authenticate(username, password, **kwargs)
        if not user: # Login failed
            self.email_user_on_failed_login(username, password, **kwargs)
        return user


    def email_user_on_failed_login(self, username, password, **kwargs):
        try:
            user = User.objects.get(username=username)
            message = render_to_string("secure_login/failed_login_user.txt")
            send_mail("failed_login", message, settings.DEFAULT_FROM_EMAIL, [user.email])

        except User.DoesNotExist:
            pass
