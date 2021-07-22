import random
import string


def generate_unique_id():
    return ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(16))
