import re
import unicodedata

import markdown
from bs4 import BeautifulSoup


def slugify(value: str, allow_unicode: bool = False):
    if allow_unicode:
        value = unicodedata.normalize('NFKC', str(value))
    else:
        value = unicodedata.normalize('NFKD', str(value)).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[-\s]+', '-', re.sub(r'[^\w\s-]', '', value.lower()).strip())


def strip_markdown(value: str):
    return BeautifulSoup(markdown.markdown(value), 'lxml').text


def to_snake_case(text: str):
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)).lower()
