from rest_framework import serializers
from .models import ShortenedURL


class ShortenedURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ['original_url', 'short_id']
