from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ShortenedURL
from .utils import generate_short_id, normalize_and_validate_url
from .serializers import ShortenedURLSerializer
from django.shortcuts import get_object_or_404, redirect


class ShortenURLView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'url': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    ))
    def post(self, request, *args, **kwargs):
        original_url = request.data.get('url')
        normalized_url = normalize_and_validate_url(original_url)
        if not normalized_url:
            return Response({'error': 'Invalid URL'}, status=status.HTTP_400_BAD_REQUEST)
        short_id = generate_short_id()
        short_url = ShortenedURL.objects.create(original_url=normalized_url, short_id=short_id)
        return Response(ShortenedURLSerializer(short_url).data)


class RedirectView(APIView):
    def get(self, request, short_id, *args, **kwargs):
        short_url = get_object_or_404(ShortenedURL, short_id=short_id)
        return redirect(short_url.original_url)
