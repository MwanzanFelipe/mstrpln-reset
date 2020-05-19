from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic
from .models import *
from .forms import *

def index(request): #the index view
    inbox_count = PostIt.objects.filter(active=True).count()
    starred_actions_count = Action.objects.filter(starred=True).count()
    top_priorities = Action.objects.filter(active=True).order_by('priority')[:5]

    return render(request, "datum/index.html", {
        "inbox_count": inbox_count,
        "starred_actions_count": starred_actions_count,
        "top_priorities": top_priorities,
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
        "text",
        "effort",
        "importance",
        "enjoyment",
        "relationship",
        "starred",
        "tags",
        "due_date"
    ]

class ActionUpdate(generic.edit.UpdateView):
    model = Action
    fields = [
        "title",
        "text",
        "effort",
        "importance",
        "enjoyment",
        "relationship",
        "starred",
        "tags",
        "due_date",
        "active",
        "complete",
        "snooze_date",
        "recurrence_date",
        "recreation_date"
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
        "text",
        "starred",
        "tags"
    ]

class InformationUpdate(generic.edit.UpdateView):
    model = Information
    fields = [
        "title",
        "text",
        "starred",
        "tags"
    ]