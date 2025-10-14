from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
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
    path('create_measurement/', views.create_measurement, name='create_measurement'),
    path("measurement/<int:pk>/", views.view_measurement, name="view_measurement"),
    path("measurement/<int:pk>/edit/", views.edit_measurement, name="edit_measurement"),
    path("measurement/<int:pk>/delete/", views.delete_measurement, name="delete_measurement"),
    path("ckeditor/upload/", views.ckeditor_upload, name="ckeditor_upload"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)