from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import PostIt

def postit_list(request):
    postits = PostIt.objects.order_by('created_date')
    return render(request, 'datum/postit_list.html', {'postits': postits})

def postit_detail(request, pk):
    postit = get_object_or_404(PostIt, pk=pk)
    return render(request, 'datum/postit_detail.html', {'postit': postit})