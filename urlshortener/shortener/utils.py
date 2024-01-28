import uuid
import string
import random


def generate_short_id(length=8):
    # Generate a random string of letters and digits
    short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return short_id
