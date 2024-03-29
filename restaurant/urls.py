from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api/opening-hours', views.OpeningHoursViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]

urlpatterns += router.urls