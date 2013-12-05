from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core import mail
from django.test.utils import override_settings
from django.conf import settings


class SecureLoginBackendTest(TestCase):

    @override_settings(SECURE_LOGIN_CHECKERS=["secure_login.checkers.no_weak_passwords", ])
    def test_no_weak_passwords(self):
        # import pdb; pdb.set_trace()
        bad_password = "albatross"
        good_password = "a-l0ng-pa55w0rd-@^&"
        user = User.objects.create(username="hello")
        user.set_password(bad_password)
        user.save()
        self.assertFalse(authenticate(username="hello", password=bad_password))

        user.set_password(good_password)
        user.save()
        self.assertEqual(authenticate(username="hello", password=good_password), user)

    @override_settings(SECURE_LOGIN_CHECKERS=["secure_login.checkers.no_short_passwords", ])
    def test_no_short_passwords(self):
        bad_password = "123"
        good_password = "a-l0ng-pa55w0rd-@^&"
        user = User.objects.create(username="hello")
        user.set_password(bad_password)
        user.save()
        self.assertFalse(authenticate(username="hello", password=bad_password))

        user.set_password(good_password)
        user.save()
        self.assertEqual(authenticate(username="hello", password=good_password), user)

    @override_settings(SECURE_LOGIN_CHECKERS=["secure_login.checkers.no_username_password_same", ])
    def test_no_username_password_same(self):
        username = "hellohello"
        bad_password = "hellohello"
        good_password = "a-l0ng-pa55w0rd-@^&"
        user = User.objects.create(username=username)
        user.set_password(bad_password)
        user.save()
        self.assertFalse(authenticate(username=username, password=bad_password))

        user.set_password(good_password)
        user.save()
        self.assertEqual(authenticate(username=username, password=good_password), user)

    @override_settings(SECURE_LOGIN_ON_FAIL=["secure_login.on_fail.email_user", ])
    def test_email_sent_on_wrong_password(self):
        username = "hello"
        password = "hellohello"
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        self.assertFalse(authenticate(username=username, password=password + "1"))
        self.assertEqual(len(mail.outbox), 1)
