from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
# router.register(r'users', views.UserViewSet)
router.register(r"booking/tables", views.BookingViewSet, basename="Booking")

urlpatterns = [
    path('', views.home, name='home'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('menu/', views.MenuItemsView.as_view()),
    path('menu/<int:pk>', views.SingleMenuItemView.as_view()),
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
]