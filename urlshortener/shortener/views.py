from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ShortenedURL
from .utils import generate_short_id
from .serializers import ShortenedURLSerializer, CreateURLSerializer
from django.shortcuts import get_object_or_404, redirect


class ShortenURLView(APIView):
    parser_classes = [JSONParser]
    def post(self, request, *args, **kwargs):
        serializer = CreateURLSerializer(data=request.data)
        if serializer.is_valid():
            original_url = serializer.validated_data['url']
            short_id = generate_short_id()
            short_url = ShortenedURL.objects.create(original_url=original_url, short_id=short_id)
            return Response(ShortenedURLSerializer(short_url).data)
        return Response(serializer.errors, status=400)


class RedirectView(APIView):
    def get(self, request, short_id, *args, **kwargs):
        short_url = get_object_or_404(ShortenedURL, short_id=short_id)
        return redirect(short_url.original_url)
