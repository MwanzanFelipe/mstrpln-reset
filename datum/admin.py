from django.contrib import admin
from .models import *

admin.site.register(PostIt)


class LogInline(admin.StackedInline):
    model = Log
    can_delete = False
    max_num = 0

class ActionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,						{'fields': ['title', 'complete', 'active', 'starred', 'text']}),
		('Characteristics',			{'fields': ['importance', 'effort', 'enjoyment', 'relationship', 'tags', 'priority'], 'classes': ['collapse']}),
		('User-generated date characteristics',	{'fields': ['due_date','snooze_date','recurrence_date'], 'classes': ['collapse']}),
		('Auto-generated date characteristics',	{'fields': ['creation_date','recreation_date','last_modified','latest_priority_calc_date'], 'classes': ['collapse']}),
	]

	inlines = [
		LogInline,
	]

	readonly_fields = ['priority','creation_date','recreation_date','last_modified','latest_priority_calc_date']

	list_display = ('title','complete','active','importance','effort','enjoyment','relationship','priority',)
	search_fields = ('title',)
	list_filter = ('complete','active',)
admin.site.register(Action,ActionAdmin)

class InformationAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,						{'fields': ['title', 'starred', 'text']}),
		('Characteristics',			{'fields': ['tags']}),
		('Auto-generated date characteristics',	{'fields': ['creation_date','last_modified'], 'classes': ['collapse']}),
	]

	readonly_fields = ['creation_date','last_modified']

	list_display = ('title','last_modified',)
admin.site.register(Information,InformationAdmin)

class LogAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,						{'fields': ['title','action']}),
		('Characteristics',			{'fields': ['importance', 'effort', 'enjoyment', 'relationship', 'tags']}),
		('Date characteristics',	{'fields': ['completion_date']}),
	]

	readonly_fields = ['title','action','importance','effort','enjoyment','relationship','tags','completion_date']

	list_display = ('title','completion_date',)
	search_fields = ('title',)
admin.site.register(Log,LogAdmin)
