from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django import forms

from .utils import get_callable

DEFAULT_ERROR_MESSAGE = "Please review the username and password"


class SecureFormMixin(object):

    def clean(self):
        DEFAULT_CHECKERS = ["secure_login.checkers.no_weak_passwords",
                            "secure_login.checkers.no_short_passwords",
                            "secure_login.checkers.no_username_password_same"]

        checkers = getattr(settings, "SECURE_LOGIN_CHECKERS", DEFAULT_CHECKERS)
        for checker in checkers:
            checker_ = get_callable(checker)
            if not checker_(**self.cleaned_data):
                raise forms.ValidationError(getattr(checker_, "error_message", DEFAULT_ERROR_MESSAGE))
        return super(SecureFormMixin, self).clean()


class SecureLoginForm(SecureFormMixin, AuthenticationForm):
    pass
