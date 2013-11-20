from django.contrib.auth import backends

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class SecureLoginBackend(backends.ModelBackend):


    def authenticate(self, username=None, password=None, **kwargs):
        if not self.no_weak_passwords(username, password, **kwargs):
            return None
        return super(SecureLoginBackend, self).authenticate(username, password, **kwargs)

    def no_weak_passwords(self, username=None, password=None, **kwargs):
        wordlist = os.path.join(BASE_DIR, "weakpasswords.txt")
        weak_passwords = [el.strip() for el in open(wordlist).read().split()]
        if password in weak_passwords:
            return False
        return True

