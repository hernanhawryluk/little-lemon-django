from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('menu/<int:pk>', views.menu_item, name='item'),
    path('reviews/', views.ReviewView.as_view(), name='review_detail'),
]