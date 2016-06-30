from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import uuid


class Distributor(models.Model):
	user = models.OneToOneField(User)
	billing_key = models.CharField(max_length=200, blank=True)
	api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

	def __unicode__(self):
		return self.user.username