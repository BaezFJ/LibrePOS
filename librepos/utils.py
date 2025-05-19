from decimal import Decimal
from typing import Union

from datetime import datetime
from zoneinfo import ZoneInfo

from flask import current_app
from slugify import slugify

CENTS_PER_DOLLAR = 100


class InvalidAmountError(ValueError):
    """Raised when the amount is invalid (negative or non-numeric)."""

    pass


def convert_dollars_to_cents(amount: Union[float, Decimal, None]) -> int:
    """
    Convert a dollar amount to cents.

    Args:
        amount: Dollar amount to convert. Can be a float, Decimal or None.

    Returns:
        int: Amount in cents (rounded down to the nearest cent)

    Raises:
        InvalidAmountError: If amount is negative

    Examples:
        >>> convert_dollars_to_cents(1.23)
        123
        >>> convert_dollars_to_cents(None)
        0
    """
    if amount is None or amount == 0:
        return 0

    try:
        decimal_amount = Decimal(str(amount))
        if decimal_amount < 0:
            raise InvalidAmountError("Amount cannot be negative")
        return int(decimal_amount * CENTS_PER_DOLLAR)
    except (TypeError, ValueError):
        raise InvalidAmountError("Invalid amount format")


def convert_cents_to_dollars(cents: Union[int, None]) -> Decimal:
    """
    Convert a cent amount to dollars.

    Args:
        cents: Amount in cents to convert. Can be an integer or None.

    Returns:
        Decimal: Amount in dollars with 2 decimal places precision

    Raises:
        InvalidAmountError: If amount is negative

    Examples:
        >>> convert_cents_to_dollars(123)
        Decimal('1.23')
        >>> convert_cents_to_dollars(None)
        Decimal('0.00')
    """
    if cents is None or cents == 0:
        return Decimal("0.00")

    try:
        if cents < 0:
            raise InvalidAmountError("Amount cannot be negative")
        return Decimal(str(cents)) / CENTS_PER_DOLLAR
    except (TypeError, ValueError):
        raise InvalidAmountError("Invalid amount format")


def timezone_aware_datetime():
    timezone = current_app.config["TIMEZONE"]

    if not timezone:
        return datetime.now(ZoneInfo("UTC"))

    return datetime.now(ZoneInfo(timezone))


def sanitize_form_data(form, exclude_fields: list[str] | None = None):
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


def slugify_string(string: str, max_length: int = 50, word_boundary: bool = True):
    return slugify(string, max_length=max_length, word_boundary=word_boundary)
