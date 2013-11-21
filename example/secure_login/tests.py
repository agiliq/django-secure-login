from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class SecureLoginBackendTest(TestCase):
    def test_no_weak_passwords(self):
        bad_password = "albatross"
        good_password = "a-l0ng-pa55w0rd-@^&"
        user = User.objects.create(username="hello")
        user.set_password("abc")
        user.save()
        self.assertFalse(authenticate(username="hello", password=bad_password))

        user.set_password(good_password)
        user.save()
        self.assertEqual(authenticate(username="hello", password=good_password), user)


    def test_no_short_passwords(self):
        bad_password = "123"
        good_password = "a-l0ng-pa55w0rd-@^&"
        user = User.objects.create(username="hello")
        user.set_password("abc")
        user.save()
        self.assertFalse(authenticate(username="hello", password=bad_password))

        user.set_password(good_password)
        user.save()
        self.assertEqual(authenticate(username="hello", password=good_password), user)
