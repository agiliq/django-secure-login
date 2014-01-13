Usage
===========

Simple
-----------

Set

    AUTHENTICATION_BACKENDS = ("secure_login.backends.SecureLoginBackend", )

Which will run all the default checkers

Advanced
--------------------

    AUTHENTICATION_BACKENDS = ("secure_login.backends.SecureLoginBackend", )

And

    SECURE_LOGIN_CHECKERS = [
        "secure_login.checkers.no_weak_passwords",
        "secure_login.checkers.no_short_passwords",
    ]

`SECURE_LOGIN_CHECKERS` should be a list of callables. Each callable should only return true if it wants the authetication to go through.

And

    SECURE_LOGIN_ON_FAIL = [
        "secure_login.on_fail.email_user",
        "secure_login.on_fail.populate_failed_requests",
    ]