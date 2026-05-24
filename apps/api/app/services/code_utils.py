import string
import random

BASE62 = string.ascii_letters + string.digits


def generate_code(length: int = 6):
    return "".join(random.choice(BASE62) for _ in range(length))