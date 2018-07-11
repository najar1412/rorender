from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pop/', views.pop, name='pop'),
    path('refresh/', views.refresh, name='refresh'),
    path('manage/', views.manage, name='manage'),
    path('make_workstation/', views.make_workstation, name='make_workstation'),
    path('make_manager/', views.make_manager, name='make_manager'),
    path('remote_connect/', views.remote_connect, name='remote_connect'),
]