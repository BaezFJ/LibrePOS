import secrets
import uuid
from datetime import datetime
from ipaddress import ip_network, ip_address

import pytz
from better_profanity import profanity
from flask import current_app
from slugify import slugify

def is_profanity(text: str) -> bool:
    """Check if the given text contains profanity."""
    return profanity.contains_profanity(text)


def censor_profanity(text: str) -> str:
    """Censor profanity in the given text."""
    return profanity.censor(text)


def generate_slug(text: str) -> str:
    """Generate a slug from the given text."""
    forbidden_words = []
    for word in text.split():
        if is_profanity(word):
            forbidden_words.append(word)
    return slugify(text, word_boundary=True, save_order=True, stopwords=forbidden_words)


def generate_uuid() -> str:
    """Generate a UUID."""
    return str(uuid.uuid4())


def generate_token(byte_size: int = 64) -> str:
    """Generate a secure token"""
    return secrets.token_hex(byte_size)


def generate_password(byte_size: int = 16) -> str:
    """Generate a secure password"""
    return secrets.token_urlsafe(byte_size)


def timezone_aware_datetime():
    """
    Generate a timezone-aware datetime object using the configured timezone.

    This function fetches the timezone configuration from the application
    configuration and applies it to the current datetime. If the configured
    timezone is invalid or cannot be recognized, UTC will be used as the fallback
    timezone.

    :return: A timezone-aware datetime object adjusted to the configured timezone
    :rtype: datetime.datetime
    """
    tz = current_app.config["TIMEZONE"]
    try:
        pytz_tz = pytz.timezone(tz)
    except pytz.exceptions.UnknownTimeZoneError:
        pytz_tz = pytz.utc
    return datetime.now(pytz_tz)


def sanitize_form_data(form, exclude_fields: list[str] = None):
    """
    Sanitizes form data by removing specified fields, including default fields such as
    CSRF token and submit button. This function is used to clean up unnecessary form data
    before further processing or saving.

    :param form: A form object that contains the data to be sanitized.
    :type form: Any
    :param exclude_fields: Optional list of field names to be excluded from the sanitized data.
    :type exclude_fields: list[str] | None
    :return: A dictionary with the sanitized form data, excluding the specified fields.
    :rtype: dict
    """
    sanitized_data = form.data

    sanitized_data.pop("csrf_token", None)
    sanitized_data.pop("submit", None)

    if exclude_fields:
        for field in exclude_fields:
            sanitized_data.pop(field, None)

    return sanitized_data


def cents_to_dollars(cents: int) -> float:
    """Convert cents to dollars."""
    return round(cents / 100, 2)


def dollars_to_cents(dollars: float) -> int:
    """Convert dollars to cents."""
    return int(dollars * 100)


def is_local_network(address):
    """Check if the given IP address is local."""
    client_ip = ip_address(address)
    local_networks = ip_network(current_app.config["LOCAL_NETWORK"])
    return any(client_ip in network for network in local_networks)


def is_allowed_ip(address):
    """Check if the given IP address is allowed."""
    return is_local_network(address) or address in current_app.config["ALLOWED_IPS"]
