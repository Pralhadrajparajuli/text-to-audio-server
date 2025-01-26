# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_active', 'is_staff']

class TextInputSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=500)