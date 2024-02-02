from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ShortenedURL
from .utils import normalize_and_validate_url


class ShortenedURLSerializer(serializers.ModelSerializer):
    original_url = serializers.CharField()

    class Meta:
        model = ShortenedURL
        fields = ['original_url', 'short_id']

    def validate_original_url(self, value):
        normalized_url = normalize_and_validate_url(value)
        if not normalized_url:
            raise serializers.ValidationError("Invalid URL")
        return normalized_url


class URLInputSerializer(serializers.Serializer):
    url = serializers.CharField()
    custom_short_id = serializers.CharField(max_length=8, required=False, allow_blank=True)

    def validate_url(self, value):
        normalized_url = normalize_and_validate_url(value)
        if not normalized_url:
            raise serializers.ValidationError("Invalid URL")
        return normalized_url


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")
