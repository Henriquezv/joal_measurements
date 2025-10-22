from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home),

    path('login/', views.login_view, name='login'),
    path('redirect/', views.redirect_after_login, name='redirect_after_login'),
    path('logout/', views.logout_view, name='logout'),

    path('manager/', views.manager, name='manager'),
    path('engineer/', views.engineer, name='engineer'),
    
    path('create_measurement/', views.create_measurement, name='create_measurement'),
    path("measurement/<int:pk>/", views.view_measurement, name="view_measurement"),
    path("measurement/<int:pk>/edit/", views.edit_measurement, name="edit_measurement"),
    path("measurement/<int:pk>/delete/", views.delete_measurement, name="delete_measurement"),
    path("measurement/<int:pk>/approve/", views.approve_measurement, name="approve_measurement"),
    path("measurement/<int:pk>/reject/", views.reject_measurement, name="reject_measurement"),
    path("ckeditor/upload/", views.ckeditor_upload, name="ckeditor_upload"),
]
