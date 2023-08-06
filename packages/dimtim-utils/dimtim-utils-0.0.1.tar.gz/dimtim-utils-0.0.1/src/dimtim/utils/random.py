import random
import string
from typing import Sequence

from django.utils.crypto import get_random_string

from common.utils.data.wordlists import ADJECTIVES, NOUNS

DEFAULT_CHARSET = string.ascii_letters + string.digits
PASSWORD_CHARSET = DEFAULT_CHARSET + string.punctuation
HEX_CHARSET = string.hexdigits


def string4(chars=DEFAULT_CHARSET):
    return get_random_string(4, chars)


def string8(chars=DEFAULT_CHARSET):
    return get_random_string(8, chars)


def string16(chars=DEFAULT_CHARSET):
    return get_random_string(16, chars)


def string32(chars=DEFAULT_CHARSET):
    return get_random_string(32, chars)


def string64(chars=DEFAULT_CHARSET):
    return get_random_string(64, chars)


def hex4(chars=HEX_CHARSET):
    return get_random_string(4, chars)


def hex8(chars=HEX_CHARSET):
    return get_random_string(8, chars)


def hex16(chars=HEX_CHARSET):
    return get_random_string(16, chars)


def hex32(chars=HEX_CHARSET):
    return get_random_string(32, chars)


def hex64(chars=HEX_CHARSET):
    return get_random_string(64, chars)


def string8upper(chars=string.ascii_uppercase + string.digits):
    return get_random_string(8, chars)


def username(underscores: bool = True):
    if underscores:
        return f'{random.choice(ADJECTIVES)}_{random.choice(ADJECTIVES)}_{random.choice(NOUNS)}'
    return f'{random.choice(ADJECTIVES).capitalize()}{random.choice(ADJECTIVES).capitalize()}{random.choice(NOUNS).capitalize()}'


def choice(variants: Sequence):
    return random.choice(variants)
