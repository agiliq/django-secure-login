Django Secure Login
=======================

Working
---------

* Ensure that passwords have a minimum length (default 6)
* Ensure that the password is not in the list of known weak passwords.
* Ensure username is not same as password

TODO
---------

* Rate limits login attempts per IP.
* Rate limits login attempts per user.
* Lockout after X failed attemps.
* Emails admins on X failed attempts.
* Email user on a failed login attempt for them.
* Integrate with fail2ban.
* Support 2F authentication
