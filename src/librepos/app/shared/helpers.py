"""Helper utilities for LibrePOS."""

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

# --- Datetime Helpers ---


def fetch_time_by_timezone(timezone: str = "America/New_York"):
    """Get current datetime in specified timezone."""
    return datetime.now(ZoneInfo(timezone))


def timedelta_months(months, compare_date=None):
    """
    Return a new datetime with a month offset applied.

    :param months: Number of months to offset
    :type months: int
    :param compare_date: Date to compare at
    :type compare_date: date
    :return: datetime
    """
    if compare_date is None:
        compare_date = date.today()

    delta = months * 365 / 12
    return compare_date + timedelta(delta)


# --- Money Helpers ---


def cents_to_dollars(cents):
    """
    Convert cents to dollars.

    :param cents: Amount in cents
    :type cents: int
    :return: float
    """
    return round(cents / 100.0, 2)


def dollars_to_cents(dollars):
    """
    Convert dollars to cents.

    :param dollars: Amount in dollars
    :type dollars: float
    :return: int
    """
    return int(dollars * 100)
