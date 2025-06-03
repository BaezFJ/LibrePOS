from decimal import Decimal
from typing import Union

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
