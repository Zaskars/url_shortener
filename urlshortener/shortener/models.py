from django.db import models
import uuid


class ShortenedURL(models.Model):
    original_url = models.URLField()
    short_id = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.original_url