import asyncio

from asgiref.sync import sync_to_async, async_to_sync
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers, status
from .models import ShortenedURL
from .utils import normalize_and_validate_url, generate_short_id, capture_screenshot_base64
from django.core.files import File
from rest_framework import serializers
from .models import ShortenedURL
from .tasks import capture_screenshot_task


def handle_url(original_url, custom_short_id=None, user=None, instance=None):
    normalized_url = normalize_and_validate_url(original_url)
    if not normalized_url:
        return {
            'error': 'Invalid URL',
            'status': status.HTTP_400_BAD_REQUEST
        }

    if custom_short_id:
        if ShortenedURL.objects.filter(short_id=custom_short_id).exists() and (
                instance is None or instance.short_id != custom_short_id):
            return {
                'error': 'Custom short ID is already in use',
                'status': status.HTTP_409_CONFLICT
            }
        short_id = custom_short_id
    else:
        short_id = generate_short_id()

    try:
        task_result = capture_screenshot_task.delay(normalized_url)
        screenshot_base64 = task_result.get(timeout=60)
    except Exception as e:
        print(e)
        screenshot_base64 = ''

    if instance is None:
        short_url = ShortenedURL.objects.create(original_url=normalized_url, short_id=short_id, user=user,
                                                screenshot=screenshot_base64)
    else:
        instance.original_url = normalized_url
        instance.short_id = short_id
        instance.screenshot = screenshot_base64
        instance.save()
        short_url = instance

    return {
        'data': URLInputSerializer(short_url).data,
        'status': status.HTTP_200_OK
    }


class URLInputSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='original_url', required=False)
    custom_short_id = serializers.CharField(max_length=16, required=False, allow_blank=True)

    class Meta:
        model = ShortenedURL
        fields = ['url', 'custom_short_id', 'short_id', 'screenshot']
        extra_kwargs = {
            'short_id': {
                'read_only': True
            },
            'screenshot': {
                'read_only': True
            }
        }

    def validate_url(self, value):
        normalized_url = normalize_and_validate_url(value)
        if not normalized_url:
            raise serializers.ValidationError("Invalid URL")
        return normalized_url

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        return handle_url(**validated_data, user=self.context['request'].user)

    def update(self, instance, validated_data):
        return handle_url(instance=instance, **validated_data, user=self.context['request'].user)


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
