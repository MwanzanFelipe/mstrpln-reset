from django.shortcuts import render

def post_list(request):
    return render(request, 'datum/post_list.html', {})
