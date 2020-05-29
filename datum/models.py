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
import math

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
class CustomTag(TagBase):
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
		CustomTag,
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
	tags = TaggableManager(through=TaggedWhatever, blank=True)

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

		# Calculate urgency based on days till due
		urgency = self.calc_urgency()

		# Calculate importance based on Action and associated tags
		scaled_importance = self.calc_scaled_importance()

		# Based on Eisenhower Matrix determine how to order Actions within the grid
		if urgency >= 2.5 and scaled_importance >= 2.5:
			base_urgency = 2.5
			base_importance = 2.5
			intercept = 0
		elif scaled_importance >= 2.5:
			base_urgency = 0
			base_importance = 2.5
			intercept = 2.5
		elif urgency >= 2.5:
			base_urgency = 2.5
			base_importance = 0
			intercept = -2.5
		else:
			base_urgency = 0
			base_importance = 0
			intercept = 0

		# Compress urgency vs scaled_importance along a slope within each Eisenhower Matrix grid
		# Measure the distance between the Action and the grid base
		pt_dist = math.sqrt((urgency - base_urgency)**2 + (scaled_importance - base_importance)**2)
		# Measure the distance between the Action and the intercept perpendicular to the slope within the grid
		ln_dist = abs(urgency - scaled_importance + intercept) / math.sqrt(2)
		# Measure the % distance along the slope within the grid (pythagorean theorem)
		priority_scale = math.sqrt(pt_dist**2 - ln_dist**2) / math.sqrt(2 * (2.5)**2)

		# Calculate the final priority by boosting the priority_scale based on the prioirity of the grid
		# Urgent + Important > Non-urgent + Important > Urgent + Unimportant > Non-urgent + Unimportant
		if urgency >= 2.5 and scaled_importance >= 2.5:
			priority = priority_scale + 3
		elif scaled_importance >= 2.5:
			priority = priority_scale + 2
		elif urgency >= 2.5:
			priority = priority_scale + 1
		else:
			priority = priority_scale

		return priority

	def calc_urgency(self):
		# Urgency ranges from 0 to 5 (and beyond) based days until due date
		# Excess of 2 weeks is minimum urgency
		if self.due_date == '' or self.due_date is None:
			days_to_expiration = 14
		else:
			days_to_expiration = self.due_date - date.today()
			days_to_expiration = days_to_expiration.days

		if days_to_expiration > 14:
			urgency = 0
		else:
			# Scale urgency from 0 to 5 and beyond
			urgency = (1 - days_to_expiration / 14) * 5
		return urgency

	def calc_scaled_importance(self):
		# Tags override Action importance. Only the most important Tag is considered
		try:
			max_impt_tag = self.tags.all().order_by('-importance').first().importance
		except:
			max_impt_tag = self.importance	

		# Action importance is a weighted average of Action importance and Max tag importance
		# Scaled importance is resized to 0-5 vs 1-5
		scaled_importance = (((self.importance * 0.25 + max_impt_tag * 0.75) - 1) / 4) * 5

		return scaled_importance

	# Toggle Snooze Data / Active Status based on characteristics
	def process_snooze(self):
		
		if self.snooze_date == "" or self.snooze_date is None:
			# If no snooze date, just pass through
			snooze_date = self.snooze_date
			active = self.active
		else:
			if self.complete == True:
				# If Task is Complete, no need for a snooze date
				snooze_date = None
				active = self.active
			else:
				if self.snooze_date <= date.today():
					# Incomplete + Snooze <= Today = Active
					active = True
					snooze_date = None
				else:
					# Incomplete + Snooze = Inactive
					active = False
					snooze_date = self.snooze_date

		return snooze_date, active

	def process_recurrence(self):
		
		if self.recurrence_date == "" or self.recurrence_date is None:
			# If no recurrence date, just pass through
			recurrence_date = self.recurrence_date
			complete = self.complete
			active = self.active
		else:
			if self.complete == True:
				if self.recurrence_date <= date.today():
					# Complete + Recurrence Date arrived/passed = Active + clear recurrence date + Incomplete
					complete = False
					recurrence_date = None
					active = True
				else:
					# Complete + Future Recurrence Date = Active + still complete + current recurrence date
					complete = True
					recurrence_date = self.recurrence_date
					active = True
			else:
				# if incomplete, no need for a recurrence date
				complete = self.complete
				recurrence_date = None
				active = self.active
		return recurrence_date, active, complete


	def save(self, **kw):
		
		# Recalculate priority when Action data changes
		self.priority = self.calced_priority()
		self.latest_priority_calc_date = timezone.now()

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

				self.starred = False

		# Process fields based on snooze and recurrence dates
		# Process recurrence impact first.
		# Snooze and recurrence should be non-interactive. Resetting task with snooze date will be cleared
		self.recurrence_date, self.active, self.complete = self.process_recurrence()
		self.snooze_date, self.active = self.process_snooze()

		# Save
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
	tags = TaggableManager(through=TaggedWhatever, blank=True)

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
	tags = TaggableManager(through=TaggedWhatever, blank=True)

	def __str__(self): 
		return "%s - %s" % (self.title, self.completion_date)

	class Meta: 
		ordering = ['-completion_date'] 
		verbose_name = "Completion Log"
