from django.contrib.auth.models import User
from django.db import models
import uuid


class ShortenedURL(models.Model):
    original_url = models.URLField()
    short_id = models.CharField(max_length=16, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    screenshot = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.original_url