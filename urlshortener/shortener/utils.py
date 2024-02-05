import uuid
import string
import random
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import hashlib
import os


def capture_screenshot_base64(url):
    service = Service(GeckoDriverManager().install())
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(url)
    driver.implicitly_wait(2)

    screenshot_base64 = driver.get_screenshot_as_base64()
    driver.quit()
    return screenshot_base64


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
