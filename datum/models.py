from django.conf import settings
from django.db import models
from django.utils import timezone


class PostIt(models.Model):
	title = models.CharField("PostIt Title", max_length=200)
	text = models.TextField("Notes", blank=True)
	creation_date = models.DateTimeField("Creation DateTime", default=timezone.now)

	active = models.BooleanField(default=True, verbose_name="Active Status")

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Post-it Note"