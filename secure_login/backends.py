from django.contrib.auth import backends
from django.conf import settings


from .utils import get_callable


class SecureLoginBackendMixin(object):

    def authenticate(self, username=None, password=None, **kwargs):
        DEFAULT_CHECKERS = ["secure_login.checkers.no_weak_passwords",
                            "secure_login.checkers.no_short_passwords",
                            "secure_login.checkers.no_username_password_same"]

        checkers = getattr(settings, "SECURE_LOGIN_CHECKERS", DEFAULT_CHECKERS)
        request = kwargs.pop('request', None)

        DEFAULT_ON_FAIL = ["secure_login.on_fail.email_user", ]
        on_fail_callables = getattr(settings,
                                    "SECURE_LOGIN_ON_FAIL",
                                    DEFAULT_ON_FAIL)

        checker_failed = False
        for checker in checkers:
            if not get_callable(checker)(username, password, **kwargs):
                checker_failed = True
                break
        if checker_failed:
            for callable_ in on_fail_callables:
                get_callable(callable_)(username, password, **kwargs)
            return None

        user = super(SecureLoginBackendMixin, self).authenticate(username,
                                                                 password,
                                                                 **kwargs)
        if not user:  # Login failed
            for callable_ in on_fail_callables:
                get_callable(callable_)(username, password, **kwargs)
        return user


class SecureLoginBackend(SecureLoginBackendMixin, backends.ModelBackend):
    pass
