from .models import *
from .views import *

# Tasks to run each day
def daily_cron_job():
	active_actions = Action.objects.filter(active=True)
	recalculate_action_priorities(active_actions)