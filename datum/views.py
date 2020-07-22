from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic
from django.apps import apps
from django.db.models import Q
from .models import *
from .forms import *


# Dashboard view
def index(request): #the index view
    # Identify all actions that have not been recalculated today

    unprocessed_actions = Action.objects.exclude(latest_priority_calc_date__date=date.today())
    recalculate_action_priorities_and_status(unprocessed_actions)

    # Active PostIt Count
    inbox_count = PostIt.objects.filter(active=True).count()

    # Orphan Action Count
    orphan_actions_count = Action.objects.filter(
        Q(active=True, complete=True, recurrence_date__isnull=True) |
        Q(active=False, complete=False, snooze_date__isnull=True)
        ).count()

    # Active Incomplete Starred Count
    starred_actions_count = Action.objects.filter(active=True, complete=False, starred=True).count()

    # Starred Tags
    starred_tags = CustomTag.objects.filter(starred=True).order_by('name')

    # Top 5 Actions Active Incomplete
    top_prioritized_actions = Action.objects.filter(active=True, complete=False).order_by('-priority')[:5]

    context = {
        "inbox_count": inbox_count,
        "starred_actions_count": starred_actions_count,
        "orphan_actions_count": orphan_actions_count,
        "top_prioritized_actions": top_prioritized_actions,
        "starred_tags": starred_tags,
        "dashboard_menu": "active"
        }

    return render(request, "datum/index.html", context)

# One Create / Edit function to rule them all
# Takes a modelname from url and optional pk
# Needed to use one GenericForm for all PostIts, Actions, and Information to enable user converting between them
# Because all PostIts, Actions, and Information use the same GenericForm, easier to process them all from one function
def GenericEdit(request, modelname=None, pk=None, template_name='datum/generic_form.html'):

    # Definition of mapping from url's modelname to form's radio button values
    model_type_dict = {
        'postit': '1',
        'action': '2',
        'information': '3'
    }
    init_model_type = model_type_dict[modelname]

    # Get the actual model object if editing an entry
    modelname_object = apps.get_model('datum', modelname)
    if modelname_object == None:
        raise Http404

    # Get the actual entry if editing
    # Setting model_object to None allows Create
    # Define form function based on Edit vs Create or modelname selected
    if pk:
        model_object = get_object_or_404(modelname_object, pk=pk)
        function = 'Edit ' + modelname_object._meta.verbose_name
    else:
        model_object = None
        function = 'Create ' + modelname_object._meta.verbose_name

    # Create a generic form
    # This controls form population if editing or creating as inital PostIt if new
    # Default form state is 1 = postit
    form = GenericForm(request.POST or None, instance=model_object, initial = {'model_type':init_model_type})

    if request.POST and form.is_valid():
        # Convert from user-supplied model_type to specific Form to save
        form_dict = {
            '1': PostItForm,
            '2': ActionForm,
            '3': InformationForm
        }
        form_class = form_dict[request.POST.get('model_type',None)]


        if init_model_type != request.POST.get('model_type',None):
            # If user-specified model_type different from initial model_type, clear model_object to allow Create, not edit
            model_object = None

            # If creating from PostIt, set PostIt as inactive
            if init_model_type == '1' and pk is not None:
                postit = PostIt.objects.get(pk=pk)
                postit.active = False
                postit.save()

        form = form_class(request.POST, instance=model_object)

        f = form.save()

        return redirect(f)

    return render(request, template_name, {
        'form': form,
        'function': function,
        })

class PostItList(generic.ListView):
    model = PostIt
    queryset = PostIt.objects.filter(active=True).order_by('creation_date')
    context_object_name = 'postits'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(PostItList, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['inbox_menu'] = 'active'
        return context

class PostItDetailView(generic.DetailView):
    model = PostIt

class ActionList(generic.ListView):
    model = Action
    context_object_name = 'actions'
    paginate_by = 5

    def get_queryset(self):
        queryset = Action.objects.filter(active=True,complete=False).order_by('-priority')
        if self.request.GET.get("subset"):
            subset = self.request.GET.get("subset")
            if subset == "Starred":
                queryset = Action.objects.filter(active=True,complete=False,starred=True).order_by('-priority')
            elif subset == "Overdue":
                queryset = Action.objects.filter(complete=False,due_date__lt=date.today()).order_by('-priority')
            elif subset == "Orphans":
                queryset = Action.objects.filter(
                    Q(active=True, complete=True, recurrence_date__isnull=True) |
                    Q(active=False, complete=False, snooze_date__isnull=True)
                    )
            elif subset == "Snoozed":
                queryset = Action.objects.filter(complete=False,snooze_date__gte=date.today()).order_by('-priority')
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ActionList, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['next_actions_menu'] = 'active'
        return context

class ActionDetailView(generic.DetailView):
    model = Action

class InformationList(generic.ListView):
    model = Information
    queryset = Information.objects.order_by('creation_date')
    context_object_name = 'information'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(InformationList, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['information_menu'] = 'active'
        return context

class InformationDetailView(generic.DetailView):
    model = Information

class LogList(generic.ListView):
    model = Log
    queryset = Log.objects.order_by('-completion_date')
    context_object_name = 'logs'
    paginate_by = 10

# Recalculate action priorities
def recalculate_action_priorities_and_status(actions):
    
    for action in actions:
        priority = action.calced_priority()
        latest_priority_calc_date = timezone.now()

        # Update instead of save so that last_modified auto_now is not triggered
        Action.objects.filter(id=action.id).update(priority=priority,latest_priority_calc_date=latest_priority_calc_date)

        # Process fields based on snooze and recurrence dates
        # Process recurrence impact first.
        # Snooze and recurrence should be non-interactive. Resetting task with snooze date will be cleared
        
        recurrence_date, active, complete = action.process_recurrence()
        Action.objects.filter(id=action.id).update(recurrence_date=recurrence_date,active=active,complete=complete)

        snooze_date, active = action.process_snooze()
        Action.objects.filter(id=action.id).update(snooze_date=snooze_date,active=active)

# List of all items by tags
class FullTagListView(generic.ListView):
    template_name = 'datum/tagitem_list.html'
    context_object_name = "actions"
    
    # Default queryset returned is Action
    def get_queryset(self):
        return Action.objects.filter(tags__slug=self.kwargs.get("slug")).all()

    def get_context_data(self, **kwargs):
        context = super(FullTagListView, self).get_context_data(**kwargs)

        # Return the Tag and Information Items along with Action
        context["tag"] = get_object_or_404(CustomTag, slug = self.kwargs.get("slug"))
        context["information"] = Information.objects.filter(tags__slug=self.kwargs.get("slug")).all()

        return context