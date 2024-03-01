from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from . models import Menu, Review
# from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ReviewSerializer
from math import ceil

# Create your views here.

def menu(request):
    menus = Menu.objects.filter(category__slug = 'food')
    drinks = Menu.objects.filter(category__slug = 'drink')
    desserts = Menu.objects.filter(category__slug = 'dessert')
    return render(request, 'menu.html', {'menus': menus, 'drinks': drinks, 'desserts': desserts })

def menu_item(request, pk):
    item = get_object_or_404(Menu, pk = pk)
    average_rating = int(ceil(item.average_rating()))
    total_reviews = item.total_reviews()
    reviews = Review.objects.filter(menu = pk).order_by('?')[:2]
    return render(request, 'menu-item.html', {'item': item, 'reviews': reviews, 'average_rating': average_rating, 'total_reviews': total_reviews})

class ReviewViews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid() and review.user == request.user:
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = self.get_object(pk)
        if review.user == request.user:
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

# ----- Django Rest Framework Generics Views -----

# class ReviewViews(generics.ListCreateAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def perform_update(self, serializer):
#         if self.get_object().user == self.request.user:
#             serializer.save()

#     def perform_destroy(self, instance):
#         if instance.user == self.request.user:
#             instance.delete()