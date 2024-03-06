from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.http import Http404
from . models import Menu, Review
from rest_framework.permissions import IsAuthenticated
from .serializers import ReviewSerializer
from math import ceil
from .serializers import MenuSerializer
from rest_framework.viewsets import ModelViewSet

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
        menu = self.request.query_params.get('menu')
        avoid = self.request.query_params.get('avoid')
        if avoid:
            avoid_list = list(filter(None, avoid.split()))
        user = self.request.query_params.get('user')

        if menu is not None:
            if user is not None:
                try:
                    review = Review.objects.filter(menu=menu, user=user)
                    if review.exists():
                        serializer = ReviewSerializer(review.first())
                        return Response(serializer.data, status=status.HTTP_200_OK)
                except:
                    return Response({'message': 'No reviews found for this user.'}, status=status.HTTP_204_NO_CONTENT)
                
            if avoid is not None:
                reviews = Review.objects.filter(menu=menu).exclude(pk__in=avoid_list)[:2]
            else:
                reviews = Review.objects.filter(menu=menu)[:2]

            if reviews.exists():
                serializer = ReviewSerializer(reviews, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else: 
                return Response({'message': 'No reviews found.'}, status=status.HTTP_200_OK)
            
        else:
            return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            if Review.objects.filter(user=request.user, menu=serializer.validated_data['menu']).exists():
                return Response({'error': 'You have already reviewed this menu item.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        review = self.get_object(request.data['pk'])
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid() and review.user == request.user:
            if Review.objects.filter(user=request.user, menu=serializer.validated_data['menu']).exists():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'You have not reviewed this menu item.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            review = Review.objects.get(pk=request.data['pk'])
            if review.user == request.user:
                review.delete()
                return Response({'message': 'Review deleted successfully.'}, status=status.HTTP_200_OK)
            else: 
                raise PermissionDenied(detail='You do not have permission to delete this review.')
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404


from random import sample

class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    
    def create(self, request, *args, **kwargs):
        return Response({'detail': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response({'detail': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response({'detail': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)