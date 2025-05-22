import uuid
from slugify import slugify


def slugify_string(string: str, max_length: int = 50, word_boundary: bool = True):
    return slugify(string, max_length=max_length, word_boundary=word_boundary)


def generate_uuid() -> str:
    return str(uuid.uuid4())
