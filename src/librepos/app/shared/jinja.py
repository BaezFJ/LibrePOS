"""Custom Jinja2 template filters for LibrePOS."""

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask

# Time units in descending order (largest first) with their seconds equivalents
TIME_UNITS: list[tuple[str, int]] = [
    ("year", 31_536_000),  # 365 days
    ("month", 2_592_000),  # 30 days
    ("week", 604_800),  # 7 days
    ("day", 86_400),  # 24 hours
    ("hour", 3_600),  # 60 minutes
    ("minute", 60),
    ("second", 1),
]


def timeago_filter(value: datetime | None, default: str = "never") -> str:
    """Convert a datetime to a human-readable "time ago" string.

    Returns the largest applicable time unit (years, months, weeks, days,
    hours, minutes, or seconds).

    Usage in templates:
        {{ user.last_login|timeago }} -> "2 hours ago"
        {{ post.created_at|timeago }} -> "3 days ago"
        {{ None|timeago("unknown") }} -> "unknown"

    Args:
        value: The datetime to convert (assumes UTC if naive)
        default: String to return if value is None

    Returns:
        Human-readable string like "2 hours ago" or "just now"
    """
    if value is None:
        return default

    # Ensure we're comparing timezone-aware datetime
    now = datetime.now(UTC)
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)

    delta_seconds = int((now - value).total_seconds())

    # Handle future dates
    if delta_seconds < 0:
        return "in the future"

    # Handle very recent times
    if delta_seconds < 1:
        return "just now"

    # Find the largest applicable time unit
    for unit_name, unit_seconds in TIME_UNITS:
        if delta_seconds >= unit_seconds:
            count = delta_seconds // unit_seconds
            plural = "s" if count != 1 else ""
            return f"{count} {unit_name}{plural} ago"

    return "just now"  # Fallback (shouldn't reach here)


def timedelta_filter(value: datetime, **kwargs) -> datetime:
    """Apply a timedelta to a datetime value.

    Usage in templates:
        {{ some_date|timedelta(days=7) }}
        {{ some_date|timedelta(hours=-2) }}
        {{ some_date|timedelta(weeks=1, days=3) }}

    Supports: days, seconds, microseconds, milliseconds,
              minutes, hours, weeks
    """
    return value + timedelta(**kwargs)


def init_jinja_filters(app: "Flask") -> None:
    """Initialize custom Jinja2 template filters.

    Call this in create_app() after init_extensions().
    """
    app.add_template_filter(timedelta_filter, name="timedelta")
    app.add_template_filter(timeago_filter, name="timeago")
