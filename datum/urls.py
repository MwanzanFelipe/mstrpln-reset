from django.urls import path
from . import views

urlpatterns = [
    path('', views.postit_list, name='postit_list'),
]