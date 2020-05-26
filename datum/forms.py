from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div
from crispy_forms.bootstrap import FormActions
from django.urls import reverse

from .models import *

# Toggle choices for input for type
CHOICES = [('1', 'PostIt'), ('2', 'Action'), ('3', 'Information')]

# Generic form to control input from PostIt, Action, and Information
class GenericForm(forms.ModelForm):
	# Add the choice field so user can select a different entry type
	model_type = forms.ChoiceField(widget=forms.RadioSelect, choices = CHOICES, initial='1')

	class Meta:
		# Build generic form off of Action because it has all possible inputs
		model = Action
		exclude = ['priority','recreation_date','last_modified','latest_priority_calc_date']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.helper = FormHelper()
		self.helper.layout = Layout(
			# Fieldset for Model Type selector
			Fieldset(
				'{{ function }}',
				'model_type'
			),

			# Fieldset for universal object data
			Fieldset(
				'Basic Info',
				'title','text',
			),

			# Fieldset for Status items
			# Collapse by default to replicate PostIt input
			Fieldset(
				'Status',
				'complete','active',
				css_class='status collapse'
			),

			# Fieldset for Category items
			# Collapse by default to replicate PostIt input
			Fieldset(
				'Categorizations',
				'starred', 'tags',
				css_class='categorizations collapse'
			),

			# Fieldset for Characteristic items
			# Collapse by default to replicate PostIt input
			Fieldset(
				'Characteristics',
				'importance','effort', 'enjoyment', 'relationship',
				css_class='characteristics collapse'
			),

			# Fieldset for Date items
			# Collapse by default to replicate PostIt input
			Fieldset(
				'Date Info',
				Div(
					'due_date','snooze_date','recurrence_date',
				),
				css_class='date_info collapse'
			),
			FormActions(
				Submit('submit', 'Submit', css_class="btn-primary save"),
			)
		)
		self.helper.form_method = 'post'

class ActionForm(forms.ModelForm):

	class Meta:
		model = Action
		fields = "__all__"

class PostItForm(forms.ModelForm):

	class Meta:
		model = PostIt
		fields = "__all__"

class InformationForm(forms.ModelForm):

	class Meta:
		model = Information
		fields = "__all__"