from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from datetime import date
from decimal import Decimal
import random

# Used for Action characteristics
LEVELS = (
	(1, '1 - Hardly'),
	(2, '2'),
	(3, '3'),
	(4, '4'),
	(5, '5 - Very'),
)

# Abstract base class so that every model gets a title, text, and creation_date
class BaseDatum(models.Model):
	title = models.CharField("Title", max_length=200)
	text = models.TextField("Notes", blank=True)
	creation_date = models.DateTimeField("Creation DateTime", auto_now_add=True)

	class Meta:
		abstract = True

# Uncharacterized items
class PostIt(BaseDatum):

	active = models.BooleanField(default=True, verbose_name="Active Status")

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Post-it Note"

	def get_absolute_url(self):
		return reverse('postit_detail', args=[self.id])

# Action items
class Action(BaseDatum): 

	# Action characteristics
	effort = models.IntegerField("Effort Level", choices = LEVELS, default = 3)
	importance = models.IntegerField("Importance", choices = LEVELS, default = 3)
	enjoyment = models.IntegerField("Enjoyment", choices = LEVELS, default = 3)
	relationship = models.IntegerField("Relationship", choices = LEVELS, default = 3)

	# Auto-calculated priority based action characteristics and other metadata
	priority = models.DecimalField("Priority Level", max_digits=6, decimal_places=2, blank=True, null=True)

	# Boolean statuses
	active = models.BooleanField(default=True, verbose_name="Active Status")
	complete = models.BooleanField("Completion Status", default=False)
	starred = models.BooleanField("Star Status", default=False)

	# Action categories
	tags = models.CharField("Tags", max_length=200, blank=True)

	# User-generated date characteristics
	due_date = models.DateField("Due Date", blank=True, null=True)
	snooze_date = models.DateField("Snooze Date", blank=True, null=True)
	recurrence_date = models.DateField("Recurrence Date", blank=True, null=True)

	# Auto-generated date characteristics
	recreation_date = models.DateTimeField("Recreation DateTime", auto_now_add=True)
	last_modified = models.DateTimeField("Last Modified", auto_now=True)
	latest_priority_calc_date = models.DateTimeField("DateTime of latest Priority Recalcuation", auto_now=True)

	# Function to calculate priority based action characteristics and other metadata
	def calced_priority(self):
		# TODO: Revise calculation based on today's date, (re)creation date, due date, importance, and tag priority
		days_since_creation = timezone.now().date() - self.recreation_date.date()
		# days_to_expiration = timezone.now().date() - self.due_date.date()
		importance = self.importance
		return Decimal(random.randint(1,1000))

	def save(self, **kw):
		
		# Recalculate priority when Action data changes
		self.priority = self.calced_priority()

		super(Action, self).save(**kw)

	def __str__(self): 
		return self.title 

	class Meta: 
		ordering = ['-priority', 'title'] 
		verbose_name = "Next Action"

	def get_absolute_url(self):
		return reverse('action_detail', args=[self.id])

class Information(BaseDatum): 

	# Boolean statuses
	starred = models.BooleanField("Star Status", default=False)

	# Information categories
	tags = models.CharField("Tags", max_length=200, blank=True)

	# Auto-generated date characteristics
	last_modified = models.DateTimeField("Last Modified", auto_now=True)

	def __str__(self): 
		return self.title 

	class Meta: 
		ordering = ['title'] 
		verbose_name = "Information Item"

	def get_absolute_url(self):
		return reverse('information_detail', args=[self.id])
