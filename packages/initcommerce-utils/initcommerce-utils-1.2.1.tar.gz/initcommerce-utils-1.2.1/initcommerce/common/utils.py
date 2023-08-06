import random
import string


def generate_random_string(length=64):
    """
    Generate a random string of the specified length.
    :param length: The length of the string to generate.
    :return: The generated string.
    """
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(length)
    )
