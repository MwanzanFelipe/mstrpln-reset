from django.urls import path
from . import views

urlpatterns = [
    path('', views.postit_list, name='postit_list'),
    path('postit/<int:pk>/', views.postit_detail, name='postit_detail'),
    path('postit/new/', views.postit_new, name='postit_new'),
    path('postit/<int:pk>/edit/', views.postit_edit, name='postit_edit'),
]