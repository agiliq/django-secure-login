from django.conf import settings

import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

wordlist = os.path.join(BASE_DIR, "weakpasswords.txt")
weak_passwords = [el.strip() for el in open(wordlist).read().split()]


def no_weak_passwords(username, password, **kwargs):
    if password in weak_passwords:
        return False
    return True


def no_short_passwords(username, password, **kwargs):
    if (len(password) <
            getattr(settings, "SECURE_LOGIN_MIN_PASSWORD_LENGTH", 6)):
        return False
    return True


def no_username_password_same(username, password, **kwargs):
    if username == password:
        return False
    return True
