from django.contrib.auth.models import User
from rest_framework import serializers
from .models import OpeningHours

class OpeningHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = '__all__'
