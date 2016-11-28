Django Secure Login
=======================

[![Build Status](https://travis-ci.org/agiliq/django-secure-login.png?branch=master)](https://travis-ci.org/agiliq/django-secure-login)
[![Coverage Status](https://coveralls.io/repos/agiliq/django-secure-login/badge.png)](https://coveralls.io/r/agiliq/django-secure-login)

Overview
------------
Django secure login provides utilities to add simple security steps around login and registration. It provides two mixins, `SecureLoginBackendMixin` and `SecureFormMixin` which check for common vulnerabilities while logging in.

* `SecureLoginBackendMixin` can be used with any Backend which has a concept of username and password
* `SecureFormMixin` can be used with any Form which has a concept of username and password. (eg login form, registration form etc)

Settings
-----------

* `SECURE_LOGIN_CHECKERS`: A list of strings which can be evaluated to callables. The callable should return True if it wants the authentication to go through.
* `SECURE_LOGIN_ON_FAIL`: A list of strings which can be evaluated to callables. Can take any action appropriate to a failed login.
* `SECURE_LOGIN_MAX_HOURLY_ATTEMPTS`: Max failed attempts per hour before the user is locked out.

Features
---------

* Works with any Backend and Form which has usename-y and password-y attributes.
* Ensure that passwords have a minimum length (default 6)
* Ensure that the password is not in the list of known weak passwords.
* Ensure username is not same as password
* Email user on a failed login attempt for them.
* Lockout after 10 failed attempts within an hour.

# Requirements

* Python (2.7, 3.4, 3.5)
* Django (1.10)

# Installation

Install using `pip`...

    pip install django_secure_login

Add `'secure_login'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
        ...
        'secure_login,
    )


Usage
-----------


Simple
===========

Set

    AUTHENTICATION_BACKENDS = ("secure_login.backends.SecureLoginBackend", )

Which will run all the default checkers.

Advanced
===========

    AUTHENTICATION_BACKENDS = ("secure_login.backends.SecureLoginBackend", )

And

    SECURE_LOGIN_CHECKERS = [
        "secure_login.checkers.no_weak_passwords",
        "secure_login.checkers.no_short_passwords",
    ]

`SECURE_LOGIN_CHECKERS` should be a list of callables. Each callable should only return true if it wants the authentication to go through.

And

    SECURE_LOGIN_ON_FAIL = [
        "secure_login.on_fail.email_user",
        "secure_login.on_fail.populate_failed_requests",
    ]

`SECURE_LOGIN_ON_FAIL` should be a list of callables. Each callable would be called in order if the authentication falls.

Writing new secure backends.
=================================

If you have an existing backend `FooBackend`, you can add SecureBackend like this.

    class SecureFooLoginBackend(SecureLoginBackendMixin, FooBackend):
        pass

If this backend has `email` as an username like identifier.

    class SecureFooLoginBackend(SecureLoginBackendMixin, FooBackend):

        def username_fieldname(self):
            return "email"



Secure Form
============

Use the `SecureFormMixin` with your usual forms. If you have an existing for `FooForm`

    class SecureFooForm(SecureFormMixin, FooForm):
        pass

If this form uses email as username lke identifier

    class SecureFooForm(SecureFormMixin, FooForm):

        def username_fieldname(self):
            return "email"



`SECURE_LOGIN_CHECKERS` will be tested in the the clean method.



TODO
---------

* Rate limits login attempts per IP.
* Rate limits login attempts per user.
* Emails admins on X failed attempts.
* Integrate with fail2ban.
* Support 2F authentication
