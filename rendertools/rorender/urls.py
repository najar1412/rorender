from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pop/', views.scan_ip_range, name='scan_ip_range'),
    path('refresh/', views.refresh, name='refresh'),
    path('manage/', views.manage, name='manage'),
    path('make_workstation/', views.make_workstation, name='make_workstation'),
    path('make_manager/', views.make_manager, name='make_manager'),
    path('make_rhino/', views.make_rhino, name='make_rhino'),
    path('make_autocad/', views.make_autocad, name='make_autocad'),
    path('remote_connect/', views.remote_connect, name='remote_connect'),
]