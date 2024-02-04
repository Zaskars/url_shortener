import django_filters
from .models import ShortenedURL
from django_filters import rest_framework as filters


class ShortenedURLFilter(filters.FilterSet):
    class Meta:
        model = ShortenedURL
        fields = {
            'original_url': ['exact', 'icontains'],
            'short_id': ['exact', 'icontains'],
        }
