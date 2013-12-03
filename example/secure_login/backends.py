from django.contrib.auth import backends
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class SecureLoginBackend(backends.ModelBackend):

    def __init__(self, *args, **kwargs):
        super(SecureLoginBackend, self).__init__(*args, **kwargs)
        wordlist = os.path.join(BASE_DIR, "weakpasswords.txt")
        self.weak_passwords = [el.strip() for el in open(wordlist).read().split()]

    def authenticate(self, username=None, password=None, **kwargs):
        if not self.no_weak_passwords(username, password, **kwargs):
            return None
        if not self.no_username_password_same(username, password, **kwargs):
            return None
        user = super(SecureLoginBackend, self).authenticate(username, password, **kwargs)
        if not user: # Login failed
            self.email_user_on_failed_login(username, password, **kwargs)
        return user




    def no_weak_passwords(self, username=None, password=None, **kwargs):

        if password in self.weak_passwords:
            return False
        return True

    def no_short_passwords(self, username=None, password=None, **kwargs):
        if len(password) < getattr(settings, "SECURE_LOGIN_MIN_PASSWORD_LENGTH", 6):
            return False
        return True

    def no_username_password_same(self, username=None, password=None, **kwargs):
        if username == password:
            return False
        return True

    def email_user_on_failed_login(self, username, password, **kwargs):
        try:
            user = User.objects.get(username=username)
            message = render_to_string("secure_login/failed_login_user.txt")
            send_mail("failed_login", message, settings.DEFAULT_FROM_EMAIL, [user.email])

        except User.DoesNotExist:
            pass
