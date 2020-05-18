from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from .forms import *

def postit_list(request):
    postits = PostIt.objects.order_by('creation_date')
    return render(request, 'datum/postit_list.html', {'postits': postits})

def postit_detail(request, pk):
    postit = get_object_or_404(PostIt, pk=pk)
    return render(request, 'datum/postit_detail.html', {'postit': postit})

def postit_new(request):
    if request.method == "POST":
        form = PostItForm(request.POST)
        if form.is_valid():
            postit = form.save(commit=False)
            postit.creation_date = timezone.now()
            postit.save()
            return redirect('postit_detail', pk=postit.pk)
    else:
        form = PostItForm()
    return render(request, 'datum/postit_edit.html', {'form': form})

def postit_edit(request, pk):
    postit = get_object_or_404(PostIt, pk=pk)
    if request.method == "POST":
        form = PostItForm(request.POST, instance=postit)
        if form.is_valid():
            postit = form.save(commit=False)
            postit.save()
            return redirect('postit_detail', pk=postit.pk)
    else:
        form = PostItForm(instance=postit)
    return render(request, 'datum/postit_edit.html', {'form': form})

def action_list(request):
    actions = Action.objects.order_by('creation_date')
    return render(request, 'datum/action_list.html', {'actions': actions})

def action_detail(request, pk):
    action = get_object_or_404(Action, pk=pk)
    return render(request, 'datum/action_detail.html', {'action': action})

def action_new(request):
    if request.method == "POST":
        form = ActionForm(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.creation_date = timezone.now()
            action.save()
            return redirect('action_detail', pk=action.pk)
    else:
        form = ActionForm()
    return render(request, 'datum/action_edit.html', {'form': form})

def action_edit(request, pk):
    action = get_object_or_404(Action, pk=pk)
    if request.method == "POST":
        form = ActionForm(request.POST, instance=action)
        if form.is_valid():
            action = form.save(commit=False)
            action.save()
            return redirect('action_detail', pk=action.pk)
    else:
        form = ActionForm(instance=action)
    return render(request, 'datum/action_edit.html', {'form': form})