"""
URL configuration for urlshortener project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import permissions

from django.urls import re_path
from drf_spectacular import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from shortener.views import RedirectView, UserRegistrationView, UserLoginView, UserURLsView, ShortURLUpdateView, \
    ShortURLDeleteView
from shortener.views import ShortenURLView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api/shorten/', ShortenURLView.as_view(), name='shorten-url'),
    path('api/urls/<str:short_id>/', ShortURLUpdateView.as_view(), name='shorturl-update'),
    path('api/urls/<str:short_id>/delete', ShortURLDeleteView.as_view(), name='shorturl-delete'),
    path('api/redirect/<short_id>/', RedirectView.as_view(), name='redirect'),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', UserLoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/my-urls/', UserURLsView.as_view(), name='my-urls'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
