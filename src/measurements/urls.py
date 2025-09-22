from django.urls import path

from django.http import HttpResponse
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('manager/', views.manager, name='manager'),
    path('home/', views.home),
    path('engineer/', views.engineer, name='engineer'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('board/', views.board, name='board'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]