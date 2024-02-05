from celery import shared_task
import asyncio
from .utils import capture_screenshot_base64


@shared_task
def capture_screenshot_task(url):
    return asyncio.run(capture_screenshot_base64(url))