from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
	path('', views.index, name='index'),

    path('<modelname>/new/', views.GenericEdit, name='generic_new'),
    path('<modelname>/<int:pk>/edit/', views.GenericEdit, name='generic_update'),

    path('postit/', views.PostItList.as_view(), name='postit_list'),
    path('postit/<int:pk>/', views.PostItDetailView.as_view(), name='postit_detail'),

    path('action/', views.ActionList.as_view(), name='action_list'),
    path('action/<int:pk>/', views.ActionDetailView.as_view(), name='action_detail'),

    path('information/', views.InformationList.as_view(), name='information_list'),
    path('information/<int:pk>/', views.InformationDetailView.as_view(), name='information_detail'),

    path('log/', views.LogList.as_view(), name='log_list'),

    path('tag/<slug:slug>/', views.FullTagListView.as_view(), name="tagged_items"),
]
