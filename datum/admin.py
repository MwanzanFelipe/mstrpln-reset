from django.contrib import admin
from .models import *

admin.site.register(PostIt)

class ActionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,						{'fields': ['title', 'complete', 'starred', 'active', 'text']}),
		('Characteristics',			{'fields': ['importance', 'effort', 'enjoyment', 'relationship', 'tags', 'priority'], 'classes': ['collapse']}),
		('Date Information',		{'fields': ['creation_date','recreation_date','last_modified','due_date', 'snooze_date','recurrence_date'], 'classes': ['collapse']}),
	]
	readonly_fields = ["priority","creation_date"]

	list_display = ('title','complete','active','importance','effort','enjoyment','relationship','priority',)
	search_fields = ('title',)
	list_filter = ('complete','active',)
admin.site.register(Action,ActionAdmin)

class InformationAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,						{'fields': ['title', 'starred', 'text']}),
		('Characteristics',			{'fields': ['tags']}),
		('Date Information',		{'fields': ['creation_date','last_modified'], 'classes': ['collapse']}),
	]	

	list_display = ('title','last_modified',)
admin.site.register(Information,InformationAdmin)