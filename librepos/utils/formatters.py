from datetime import datetime
from zoneinfo import ZoneInfo

from flask import current_app


def timezone_aware_datetime() -> datetime:
    """Return a timezone-aware datetime object."""
    timezone = current_app.config["TIMEZONE"]

    return datetime.now(ZoneInfo(timezone))
