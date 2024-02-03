import uuid
import string
import random
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests
from rest_framework import status



def page_exists(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code < 400:
            return url
    except requests.RequestException:
        pass


def generate_short_id(length=8):
    short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return short_id


def normalize_and_validate_url(url):
    if not urlparse(url).scheme:
        url = 'http://' + url

    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        return None

    if page_exists(url):
        return url
