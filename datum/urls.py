from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
	path('', views.index, name='index'),

    path('postit/', views.PostItList.as_view(), name='postit_list'),
    path('postit/<int:pk>/', views.PostItDetailView.as_view(), name='postit_detail'),
    path('postit/new/', views.PostItNew.as_view(), name='postit_new'),
    path('postit/<int:pk>/edit/', views.PostItUpdate.as_view(), name='postit_update'),

    path('action/', views.ActionList.as_view(), name='action_list'),
    path('action/<int:pk>/', views.ActionDetailView.as_view(), name='action_detail'),
    path('action/new/', views.ActionNew.as_view(), name='action_new'),
    path('action/<int:pk>/edit/', views.ActionUpdate.as_view(), name='action_update'),

    path('information/', views.InformationList.as_view(), name='information_list'),
    path('information/<int:pk>/', views.InformationDetailView.as_view(), name='information_detail'),
    path('information/new/', views.InformationNew.as_view(), name='information_new'),
    path('information/<int:pk>/edit/', views.InformationUpdate.as_view(), name='information_update'),
]
