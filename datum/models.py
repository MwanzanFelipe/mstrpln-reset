from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from datetime import date
from decimal import Decimal

LEVELS = (
	(1, '1 - Hardly'),
	(2, '2'),
	(3, '3'),
	(4, '4'),
	(5, '5 - Very'),
)

class BaseDatum(models.Model):
	title = models.CharField("Title", max_length=200)
	text = models.TextField("Notes", blank=True)
	creation_date = models.DateTimeField("Creation DateTime", default=timezone.now)

	class Meta:
		abstract = True

class PostIt(BaseDatum):

	active = models.BooleanField(default=True, verbose_name="Active Status")

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Post-it Note"

	def get_absolute_url(self):
		return reverse('postit_detail', args=[self.id])

class Action(BaseDatum): 

	effort = models.IntegerField("Effort Level", choices = LEVELS, default = 3)
	importance = models.IntegerField("Importance", choices = LEVELS, default = 3)
	enjoyment = models.IntegerField("Enjoyment", choices = LEVELS, default = 3)
	relationship = models.IntegerField("Relationship", choices = LEVELS, default = 3)

	priority = models.DecimalField("Priority Level", max_digits=6, decimal_places=2, blank=True, null=True)

	active = models.BooleanField(default=True, verbose_name="Active Status")
	complete = models.BooleanField("Completion Status", default=False)
	starred = models.BooleanField("Star Status", default=False)

	last_modified = models.DateTimeField("Last Modified", default=timezone.now)
	tags = models.CharField("Tags", max_length=200, blank=True)

	due_date = models.DateField("Due Date", blank=True, null=True)
	snooze_date = models.DateField("Snooze Date", blank=True, null=True)
	recurrence_date = models.DateField("Recurrence Date", blank=True, null=True)
	recreation_date = models.DateTimeField("Recreation DateTime", default=timezone.now)

	def calc_priority(self):
		days_since_creation = timezone.now().date() - self.recreation_date.date()
		days_to_expiration = timezone.now().date() - self.due_date.date()
		importance = self.importance

		self.priority = Decimal(days_since_creation, 2)


	def save(self, **kw):
		self.last_modified = timezone.now()
		super(Action, self).save(**kw)

	def __str__(self): 
		return self.title 

	class Meta: 
		ordering = ['-priority', 'title'] 
		verbose_name = "Next Action"

	def get_absolute_url(self):
		return reverse('action_detail', args=[self.id])

class Information(BaseDatum): 

	starred = models.BooleanField("Star Status", default=False)

	last_modified = models.DateTimeField("Last Modified", default=timezone.now)
	tags = models.CharField("Tags", max_length=200, blank=True)

	def __str__(self): 
		return self.title 

	class Meta: 
		ordering = ['title'] 
		verbose_name = "Information Item"

	def get_absolute_url(self):
		return reverse('information_detail', args=[self.id])
