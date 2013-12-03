from django.contrib.auth import backends
from django.conf import settings


DEFAULT_CHECKERS = ["secure_login.checkers.no_weak_passwords",
                    "secure_login.checkers.no_short_passwords",
                    "secure_login.checkers.no_username_password_same"]

checkers = getattr(settings, "SECURE_LOGIN_CHECKERS", DEFAULT_CHECKERS)

DEFAULT_ON_FAIL = ["secure_login.on_fail.email_user",]
on_fail_callables = getattr(settings, "SECURE_LOGIN_ON_FAIL", DEFAULT_ON_FAIL)

def get_callable(callable_str):
    path = callable_str.split(".")
    module_name = ".".join(path[:-1])
    callable_name = path[-1]
    module = __import__(module_name, {}, {}, [callable_name])
    callable_ = getattr(module, callable_name)
    return callable_


class SecureLoginBackendMixin(object):

    def authenticate(self, username=None, password=None, **kwargs):
        for checker in checkers:
            if not get_callable(checker)(username, password, **kwargs):
                return None
        user = super(SecureLoginBackendMixin, self).authenticate(username, password, **kwargs)
        if not user: # Login failed
            for callable_ in on_fail_callables:
                get_callable(callable_)(username, password, **kwargs)
        return user


class SecureLoginBackend(SecureLoginBackendMixin, backends.ModelBackend):
    pass
