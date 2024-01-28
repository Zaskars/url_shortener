from django.db import models
import uuid


class ShortenedURL(models.Model):
    original_url = models.URLField()
    short_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.original_url