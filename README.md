Django Secure Login
=======================

[![Build Status](https://travis-ci.org/agiliq/django-secure-login.png?branch=master)](https://travis-ci.org/agiliq/django-secure-login)
[![Coverage Status](https://coveralls.io/repos/agiliq/django-secure-login/badge.png)](https://coveralls.io/r/agiliq/django-secure-login)

Working
---------

* Ensure that passwords have a minimum length (default 6)
* Ensure that the password is not in the list of known weak passwords.
* Ensure username is not same as password
* Email user on a failed login attempt for them.
* Lockout after 10 failed attemps within an hour.

TODO
---------

* Rate limits login attempts per IP.
* Rate limits login attempts per user.
* Emails admins on X failed attempts.
* Integrate with fail2ban.
* Support 2F authentication
