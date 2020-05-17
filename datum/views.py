from django.shortcuts import render
from django.utils import timezone
from .models import PostIt

def postit_list(request):
    postits = PostIt.objects.order_by('created_date')
    return render(request, 'datum/postit_list.html', {'postits': postits})