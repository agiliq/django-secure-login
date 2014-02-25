from django.conf import settings


def get_callable(callable_str):
    path = callable_str.split(".")
    module_name = ".".join(path[:-1])
    callable_name = path[-1]
    module = __import__(module_name, {}, {}, [callable_name])
    callable_ = getattr(module, callable_name)
    return callable_


def handle_fieldname(username_field, password_field, func):
    def deco(**kwargs):
        username = kwargs.get(username_field)
        password = kwargs.get(password_field)
        if username:
            del kwargs[username_field]
        if password:
            del kwargs[password_field]
        return func(username, password, **kwargs)
    return deco
