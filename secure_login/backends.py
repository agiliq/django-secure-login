from django.contrib.auth import backends
from django.conf import settings


from .utils import get_callable, handle_fieldname


class SecureLoginBackendMixin(object):

    def authenticate(self, **kwargs):
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
            checker_ = self.get_final_callable(checker)
            if not checker_(**kwargs):
                checker_failed = True
                break
        if checker_failed:
            for callable_ in on_fail_callables:
                self.get_final_callable(callable_)(**kwargs)
            return None

        user = super(SecureLoginBackendMixin, self).authenticate(**kwargs)

        if not user:  # Login failed
            for callable_ in on_fail_callables:
                callable_ = self.get_final_callable(callable_)
                callable_(**kwargs)
        return user

    def username_fieldname(self):
        return "username"

    def password_fieldname(self):
        return "password"

    def get_final_callable(self, checker):
        checker_ = get_callable(checker)
        return handle_fieldname(self.username_fieldname(), self.password_fieldname(), checker_)


class SecureLoginBackend(SecureLoginBackendMixin, backends.ModelBackend):
    pass
