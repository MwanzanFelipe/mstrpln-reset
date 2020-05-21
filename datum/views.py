from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic
from .models import *
from .forms import *

# Dashboard view
def index(request): #the index view
    # TODO: recalculate_priorities(actions_where_latest_priority_calc_date_isnot_today)

    # Active PostIt Count
    inbox_count = PostIt.objects.filter(active=True).count()

    # Active Starred Count
    starred_actions_count = Action.objects.filter(active=True, starred=True).count()

    # Top 5 Actions
    top_prioritized_actions = Action.objects.filter(active=True).order_by('priority')[:5]

    return render(request, "datum/index.html", {
        "inbox_count": inbox_count,
        "starred_actions_count": starred_actions_count,
        "top_prioritized_actions": top_prioritized_actions,
        })

class PostItList(generic.ListView):
    model = PostIt
    queryset = PostIt.objects.filter(active=True).order_by('creation_date')
    context_object_name = 'postits'
    paginate_by = 5

class PostItDetailView(generic.DetailView):
    model = PostIt

class PostItNew(generic.edit.CreateView):
    model = PostIt
    fields = [
        "title",
        "text"
    ] 

class PostItUpdate(generic.edit.UpdateView):
    model = PostIt
    fields = [
        "title",
        "text",
        "active"
    ] 

class ActionList(generic.ListView):
    model = Action
    queryset = Action.objects.filter(active=True).order_by('creation_date')
    context_object_name = 'actions'
    paginate_by = 5

class ActionDetailView(generic.DetailView):
    model = Action

class ActionNew(generic.edit.CreateView):
    model = Action
    fields = [
        "title",
        "starred",
        "text",
        "importance",
        "effort",
        "enjoyment",
        "relationship",
        "tags",
        "due_date"
    ]

class ActionUpdate(generic.edit.UpdateView):
    model = Action
    fields = [
        "title",
        "complete",
        "active",
        "starred",
        "text",
        "importance",
        "effort",
        "enjoyment",
        "relationship",
        "tags",
        "due_date",
        "snooze_date",
        "recurrence_date"
    ]

class InformationList(generic.ListView):
    model = Information
    queryset = Information.objects.order_by('creation_date')
    context_object_name = 'information'
    paginate_by = 5

class InformationDetailView(generic.DetailView):
    model = Information

class InformationNew(generic.edit.CreateView):
    model = Information
    fields = [
        "title",
        "starred",
        "text",
        "tags"
    ]

class InformationUpdate(generic.edit.UpdateView):
    model = Information
    fields = [
        "title",
        "starred",
        "text",
        "tags"
    ]

class LogList(generic.ListView):
    model = Log
    queryset = Log.objects.order_by('-completion_date')
    context_object_name = 'logs'
    paginate_by = 10

# Recalculate action priorities
def recalculate_action_priorities(actions):
    
    for action in actions:
        priority = action.calced_priority()
        latest_priority_calc_date = timezone.now()

        # Update instead of save so that last_modified auto_now is not triggered
        Action.objects.filter(id=action.id).update(priority=priority,latest_priority_calc_date=latest_priority_calc_date)