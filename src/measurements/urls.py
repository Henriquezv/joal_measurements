from django.urls import path

from django.http import HttpResponse
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('manager/', views.manager, name='manager'),
    path('home/', views.home),
    path('engineer/', views.engineer, name='Engineer'),
    path('dashboard/', views.dashboard, name='Dashboard'),
    path('board/', views.board, name='Board'),
]