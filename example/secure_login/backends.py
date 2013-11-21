from django.contrib.auth import backends
from django.conf import settings

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class SecureLoginBackend(backends.ModelBackend):

    def __init__(self, *args, **kwargs):
        super(SecureLoginBackend, self).__init__(*args, **kwargs)
        wordlist = os.path.join(BASE_DIR, "weakpasswords.txt")
        self.weak_passwords = [el.strip() for el in open(wordlist).read().split()]

    def authenticate(self, username=None, password=None, **kwargs):
        if not self.no_weak_passwords(username, password, **kwargs):
            return None
        return super(SecureLoginBackend, self).authenticate(username, password, **kwargs)

    def no_weak_passwords(self, username=None, password=None, **kwargs):

        if password in self.weak_passwords:
            return False
        return True

    def no_short_passwords(self, username=None, password=None, **kwargs):
        if len(password) <

