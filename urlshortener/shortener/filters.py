import django_filters
from .models import ShortenedURL


class ShortenedURLFilter(django_filters.FilterSet):
    class Meta:
        model = ShortenedURL
        fields = {
            'original_url': ['exact', 'contains'],
            'short_id': ['exact'],
        }
