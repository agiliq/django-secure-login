from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core import mail
from django.test.utils import override_settings

class SecureLoginBackendTest(TestCase):
    def test_no_weak_passwords(self):
        bad_password = "albatross"
        good_password = "a-l0ng-pa55w0rd-@^&"
        user = User.objects.create(username="hello")
        user.set_password(bad_password)
        user.save()
        self.assertFalse(authenticate(username="hello", password=bad_password))

        user.set_password(good_password)
        user.save()
        self.assertEqual(authenticate(username="hello", password=good_password), user)


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

    def test_email_sent_on_wrong_password(self):
        username = "hello"
        password = "hellohello"
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        self.assertFalse(authenticate(username=username, password=password+"1"))
        self.assertEqual(len(mail.outbox), 1)
