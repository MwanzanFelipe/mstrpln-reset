from django import forms

from .models import *

class PostItForm(forms.ModelForm):

    class Meta:
        model = PostIt
        fields = ('title', 'text', 'active')

class ActionForm(forms.ModelForm):

    class Meta:
        model = Action
        fields = ('title', 'text','effort','importance'
        	,'enjoyment','relationship','active','complete'
        	,'starred','tags','due_date','snooze_date','recurrence_date','recreation_date')