from rest_framework import serializers
from .models import Menu, Review

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['menu', 'rating', 'comment', 'created', 'updated']
        read_only_fields = ['user']