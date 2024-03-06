from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.signup_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('api/login', views.login_api),
    path('api/signup', views.signup_api),
    path('api/test-token', views.test_token_api),
]