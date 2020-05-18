from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),

    path('postit/', views.postit_list, name='postit_list'),
    path('postit/<int:pk>/', views.postit_detail, name='postit_detail'),
    path('postit/new/', views.postit_new, name='postit_new'),
    path('postit/<int:pk>/edit/', views.postit_edit, name='postit_edit'),

    path('action/', views.action_list, name='action_list'),
    path('action/<int:pk>/', views.action_detail, name='action_detail'),
    path('action/new/', views.action_new, name='action_new'),
    path('action/<int:pk>/edit/', views.action_edit, name='action_edit'),
]