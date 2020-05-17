from django.urls import path
from . import views

urlpatterns = [
    path('', views.postit_list, name='postit_list'),
    path('postit/<int:pk>/', views.postit_detail, name='postit_detail'),
]