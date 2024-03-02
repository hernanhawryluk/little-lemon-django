from rest_framework import serializers
from .models import Menu, Review

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    pk = serializers.ReadOnlyField()
    
    class Meta:
        model = Review
        fields = ['pk', 'user', 'menu', 'rating', 'comment', 'created', 'updated']
