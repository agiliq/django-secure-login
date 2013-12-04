Django Secure Login
=======================

[![Build Status](https://travis-ci.org/agiliq/django-secure-login.png?branch=master)](https://travis-ci.org/agiliq/django-secure-login)

Working
---------

* Ensure that passwords have a minimum length (default 6)
* Ensure that the password is not in the list of known weak passwords.
* Ensure username is not same as password
* Email user on a failed login attempt for them.

TODO
---------

* Rate limits login attempts per IP.
* Rate limits login attempts per user.
* Lockout after X failed attemps.
* Emails admins on X failed attempts.
* Integrate with fail2ban.
* Support 2F authentication
