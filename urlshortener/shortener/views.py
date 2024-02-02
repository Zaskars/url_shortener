from django.contrib.auth import authenticate
from drf_spectacular import openapi
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ShortenedURL
from .utils import generate_short_id, normalize_and_validate_url
from .serializers import ShortenedURLSerializer, UserRegistrationSerializer, UserLoginSerializer, URLInputSerializer
from django.shortcuts import get_object_or_404, redirect


class ShortenURLView(GenericAPIView):
    serializer_class = URLInputSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            original_url = serializer.validated_data['url']
            normalized_url = normalize_and_validate_url(original_url)
            custom_short_id = serializer.validated_data.get('custom_short_id')

            if not normalized_url:
                return Response({
                                    'error': 'Invalid URL'
                                }, status=status.HTTP_400_BAD_REQUEST)

            short_id = custom_short_id if custom_short_id else generate_short_id()

            if custom_short_id and ShortenedURL.objects.filter(short_id=custom_short_id).exists():
                return Response({
                    'error': 'Custom short ID is (вроде is надо) already in use'
                }, status=status.HTTP_409_CONFLICT)

            short_url = ShortenedURL.objects.create(original_url=normalized_url, short_id=short_id, user=request.user)
            return Response(ShortenedURLSerializer(short_url).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RedirectView(APIView):
    def get(self, request, short_id, *args, **kwargs):
        short_url = get_object_or_404(ShortenedURL, short_id=short_id)
        return redirect(short_url.original_url)


class UserRegistrationView(GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class UserURLsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShortenedURLSerializer

    def get(self, request, *args, **kwargs):
        urls = ShortenedURL.objects.filter(user=request.user)
        serializer = self.get_serializer(urls, many=True)
        return Response(serializer.data)


# TODO добавить валидацию как при создании ссылки
class ShortURLUpdateView(RetrieveUpdateAPIView):
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer
    lookup_field = 'short_id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ShortURLDeleteView(DestroyAPIView):
    queryset = ShortenedURL.objects.all()
    lookup_field = 'short_id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
