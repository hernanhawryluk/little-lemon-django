from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('api/menu', views.MenuViewSet)

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('menu/<int:pk>', views.menu_item, name='item'),
    path('api/review/', views.ReviewViews.as_view(), name='review'),
    # path('api/review/', views.ReviewAPIViews.as_view())
]

urlpatterns += router.urls
