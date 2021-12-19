import os
import random
import string

script_dir = os.path.dirname(os.path.realpath(__file__))


def random_string(length: int) -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
