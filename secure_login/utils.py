def get_callable(callable_str):
    path = callable_str.split(".")
    module_name = ".".join(path[:-1])
    callable_name = path[-1]
    module = __import__(module_name, {}, {}, [callable_name])
    callable_ = getattr(module, callable_name)
    return callable_
