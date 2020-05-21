from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from datetime import date
from decimal import Decimal
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase
import random

# from taggit.models import TaggedItem

# Used for Action characteristics
LEVELS = (
	(1, '1 - Hardly'),
	(2, '2'),
	(3, '3'),
	(4, '4'),
	(5, '5 - Very'),
)

# Custom Tag which includes extra fields
class Tag(TagBase):
	text = models.TextField("Notes", blank=True)

	# Tag characteristics
	importance = models.IntegerField("Importance", choices = LEVELS, default = 3)

	# Boolean statuses
	starred = models.BooleanField("Star Status", default=False)

	class Meta:
		verbose_name = _("Tag")
		verbose_name_plural = _("Tags")

# Interim custom tag model allowing multiple models to utilize custom tag
class TaggedWhatever(GenericTaggedItemBase):
	tag = models.ForeignKey(
		Tag,
		on_delete=models.CASCADE,
		related_name="%(app_label)s_%(class)s_items")

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
	tags = TaggableManager(through=TaggedWhatever)

	# User-generated date characteristics
	due_date = models.DateField("Due Date", blank=True, null=True)
	snooze_date = models.DateField("Snooze Date", blank=True, null=True)
	recurrence_date = models.DateField("Recurrence Date", blank=True, null=True)

	# Auto-generated date characteristics
	recreation_date = models.DateTimeField("Recreation DateTime", auto_now_add=True, editable=False)
	last_modified = models.DateTimeField("Last Modified", auto_now=True, editable=False)
	latest_priority_calc_date = models.DateTimeField("DateTime of latest Priority Recalcuation", auto_now=True, editable=False)

	# Cache initial version of record to determine before/after differences
	def __init__(self, *args, **kw):

		super(Action, self).__init__(*args, **kw)

		# Define fields that may trigger actions on change
		self.__trigger_fields = ['active','complete','due_date','snooze_date','recurrence_date']

		# Create object of initial trigger-field values
		for field in self.__trigger_fields:
			setattr(self, '__original_%s' % field, getattr(self, field))

	# Function to calculate priority based action characteristics and other metadata
	def calced_priority(self):
		# TODO: Revise calculation based on today's date, (re)creation date, due date, importance, and tag priority
		# days_since_creation = timezone.now().date() - self.recreation_date.date()
		# days_to_expiration = timezone.now().date() - self.due_date.date()
		importance = self.importance
		return Decimal(random.randint(1,1000))

	def save(self, **kw):
		
		# Recalculate priority when Action data changes
		self.priority = self.calced_priority()

		# Save
		super(Action, self).save(**kw)

		if self.complete:
			# If going from incomplete to complete
			if getattr(self, '__original_complete') != getattr(self,'complete'):
				# Add a log entry when Actions are marked complete
				# This works but would perhaps be better if functionality is "owned" by Log
				# Could use post_save.connect to trigger Log. Especially better if post-save logging needed for multiple models
				# Given that Log is only used for Action, leaving this for now unless Action model gets too busy
				l = Log.objects.create(
					action = self,
					title = self.title,
					completion_date = date.today(),
					effort = self.effort,
					importance = self.importance,
					enjoyment = self.enjoyment,
					relationship = self.relationship
				)

				# Add Action's tags to Log object
				l.tags.add(*self.tags.all())

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
	tags = TaggableManager(through=TaggedWhatever)

	# Auto-generated date characteristics
	last_modified = models.DateTimeField("Last Modified", auto_now=True, editable=False)

	def __str__(self): 
		return self.title 

	class Meta: 
		ordering = ['title'] 
		verbose_name = "Information Item"

	def get_absolute_url(self):
		return reverse('information_detail', args=[self.id])

# Log of Action completions
class Log(models.Model):
	title = models.CharField("Title", max_length=200, editable=False)
	completion_date = models.DateTimeField("Completion DateTime", auto_now_add=True, editable=False)

	# Link to originating Action
	action = models.ForeignKey(Action, null=True, on_delete=models.SET_NULL)

	# Action characteristics
	effort = models.IntegerField("Effort Level", choices = LEVELS, editable=False)
	importance = models.IntegerField("Importance", choices = LEVELS, editable=False)
	enjoyment = models.IntegerField("Enjoyment", choices = LEVELS, editable=False)
	relationship = models.IntegerField("Relationship", choices = LEVELS, editable=False)

	# Action categories
	tags = TaggableManager(through=TaggedWhatever)

	def __str__(self): 
		return "%s - %s" % (self.title, self.completion_date)

	class Meta: 
		ordering = ['-completion_date'] 
		verbose_name = "Completion Log"
