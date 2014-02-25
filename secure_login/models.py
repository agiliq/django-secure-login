from django.db import models

from django.contrib.auth.models import User


class FailedLogin(models.Model):
    attempted_at = models.DateTimeField(auto_now=True)
    for_user = models.ForeignKey(User, null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
