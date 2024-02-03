from django.contrib.auth import authenticate
from drf_spectacular import openapi
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ShortenedURL
from .utils import generate_short_id, normalize_and_validate_url
from .serializers import UserRegistrationSerializer, UserLoginSerializer, URLInputSerializer, handle_url
from django.shortcuts import get_object_or_404, redirect


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'


class ShortenURLView(GenericAPIView):
    serializer_class = URLInputSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = handle_url(serializer.validated_data['original_url'],
                                custom_short_id=serializer.validated_data.get('custom_short_id'),
                                user=request.user)
            if 'error' in result:
                return Response({
                                    'error': result['error']
                                }, status=result['status'])
            return Response(result['data'], status=result['status'])
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
    serializer_class = URLInputSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        urls = ShortenedURL.objects.filter(user=request.user)
        page = self.paginate_queryset(urls)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(urls, many=True)
        return Response(serializer.data)


# TODO добавить валидацию как при создании ссылки
class ShortURLUpdateView(RetrieveUpdateAPIView):
    queryset = ShortenedURL.objects.all()
    serializer_class = URLInputSerializer
    lookup_field = 'short_id'
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            result = handle_url(serializer.validated_data.get('original_url', instance.original_url),
                                custom_short_id=serializer.validated_data.get('custom_short_id', instance.short_id),
                                user=request.user, instance=instance)
            if 'error' in result:
                return Response({
                                    'error': result['error']
                                }, status=result['status'])
            return Response(result['data'], status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShortURLDeleteView(DestroyAPIView):
    queryset = ShortenedURL.objects.all()
    lookup_field = 'short_id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
