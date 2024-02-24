from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu'),
    path('booking/', login_required(views.booking), name='booking'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
]