from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core import mail
from django.test.utils import override_settings
from django.conf import settings
from django import forms

from .models import FailedLogin
from .forms import SecureLoginForm, SecureFormMixin


class SecureLoginBackendTest(TestCase):

    @override_settings(SECURE_LOGIN_CHECKERS=["secure_login.checkers.no_weak_passwords", ])
    def test_no_weak_passwords(self):
        bad_password = "albatross"
        good_password = "a-l0ng-pa55w0rd-@^&"
        user = User.objects.create(username="hello")
        user.set_password(bad_password)
        user.save()
        self.assertFalse(authenticate(username="hello", password=bad_password))

        user.set_password(good_password)
        user.save()
        self.assertEqual(
            authenticate(username="hello", password=good_password), user)

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
        self.assertEqual(
            authenticate(username="hello", password=good_password), user)

    @override_settings(SECURE_LOGIN_CHECKERS=["secure_login.checkers.no_username_password_same", ])
    def test_no_username_password_same(self):
        username = "hellohello"
        bad_password = "hellohello"
        good_password = "a-l0ng-pa55w0rd-@^&"
        user = User.objects.create(username=username)
        user.set_password(bad_password)
        user.save()
        self.assertFalse(
            authenticate(username=username, password=bad_password))

        user.set_password(good_password)
        user.save()
        self.assertEqual(
            authenticate(username=username, password=good_password), user)

    @override_settings(SECURE_LOGIN_ON_FAIL=["secure_login.on_fail.email_user", ])
    def test_email_sent_on_wrong_password(self):
        username = "hello"
        password = "hellohello"
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        self.assertFalse(
            authenticate(username=username, password=password + "1"))
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(SECURE_LOGIN_ON_FAIL=["secure_login.on_fail.populate_failed_requests"], SECURE_LOGIN_CHECKERS=[])
    def test_populate_failed_requests(self):
        username = "hello"
        password = "hellohello"
        user = User.objects.create_user(username=username, password=password)

        authenticate(username=username, password="not-the-correct-password")
        self.assertEqual(FailedLogin.objects.count(), 1)

    @override_settings(SECURE_LOGIN_ON_FAIL=["secure_login.on_fail.populate_failed_requests", "secure_login.on_fail.lockout_on_many_wrong_password", ], SECURE_LOGIN_CHECKERS=[])
    def test_lockout(self):
        username = "hello"
        password = "hellohello"
        user = User.objects.create_user(username=username, password=password)

        for _ in range(11):
            authenticate(
                username=username, password="not-the-correct-password")
        user_ = authenticate(username=username, password=password)
        self.assertFalse(user_.is_active)


class FormsTest(TestCase):

    @override_settings(SECURE_LOGIN_CHECKERS=["secure_login.checkers.no_weak_passwords", ])
    def test_no_weak_passwords(self):
        bad_password = "albatross"
        good_password = "a-l0ng-pa55w0rd-@^&"

        user = User.objects.create(username="hello")
        user.set_password(bad_password)
        user.save()

        form = SecureLoginForm(
            data={"username": "hello", "password": bad_password})
        self.assertFalse(form.is_valid())

        user.set_password(good_password)
        user.save()
        form = SecureLoginForm(
            data={"username": "hello", "password": good_password})
        self.assertTrue(form.is_valid())

    @override_settings(SECURE_LOGIN_CHECKERS=["secure_login.checkers.no_short_passwords", ])
    def test_no_short_passwords(self):
        bad_password = "123"
        good_password = "a-l0ng-pa55w0rd-@^&"
        user = User.objects.create(username="hello")
        user.set_password(bad_password)
        user.save()
        form = SecureLoginForm(
            data={"username": "hello", "password": bad_password})

        self.assertFalse(form.is_valid())

        user.set_password(good_password)
        user.save()
        form = SecureLoginForm(
            data={"username": "hello", "password": good_password})
        self.assertTrue(form.is_valid())

    def test_register_form(self):
        class RegiterForm(forms.Form):
            username = forms.CharField(max_length=50)
            password = forms.CharField()
            email = forms.EmailField(required=False)

        class SecureRegisterForm(SecureFormMixin, RegiterForm):
            pass

        bad_password = "albatross"

        with self.settings(SECURE_LOGIN_CHECKERS=["secure_login.checkers.no_weak_passwords", ]):
            form = SecureRegisterForm(
                data={"username": "hello", "password": bad_password})
            self.assertFalse(form.is_valid())

        with self.settings(SECURE_LOGIN_CHECKERS=[]):
            form = SecureRegisterForm(
                data={"username": "hello", "password": bad_password})
            self.assertTrue(form.is_valid())

        bad_password = 123
        with self.settings(SECURE_LOGIN_CHECKERS=["secure_login.checkers.no_short_passwords", ]):
            form = SecureRegisterForm(
                data={"username": "hello", "password": bad_password})
            self.assertFalse(form.is_valid())

        with self.settings(SECURE_LOGIN_CHECKERS=[]):
            form = SecureRegisterForm(
                data={"username": "hello", "password": bad_password})
            self.assertTrue(form.is_valid())
