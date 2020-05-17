from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import PostIt
from .forms import PostItForm

def postit_list(request):
    postits = PostIt.objects.order_by('created_date')
    return render(request, 'datum/postit_list.html', {'postits': postits})

def postit_detail(request, pk):
    postit = get_object_or_404(PostIt, pk=pk)
    return render(request, 'datum/postit_detail.html', {'postit': postit})

def postit_new(request):
    if request.method == "POST":
        form = PostItForm(request.POST)
        if form.is_valid():
            postit = form.save(commit=False)
            postit.created_date = timezone.now()
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
            postit.created_date = timezone.now()
            postit.save()
            return redirect('postit_detail', pk=postit.pk)
    else:
        form = PostItForm(instance=postit)
    return render(request, 'datum/postit_edit.html', {'form': form})