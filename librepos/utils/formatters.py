from datetime import datetime

from .financial import convert_cents_to_dollars


def receipt_number_formatter(prefix: str, counter: int, suffix: str = "") -> str:
    prefix = f"{prefix:02d}"
    number_part = f"{counter:04d}"
    return f"{prefix}-{number_part}{suffix}" if suffix else f"{prefix}-{number_part}"


def datetime_formatter(value: datetime | None, format_spec: str) -> str:
    available_formats = {
        "short-date": "%y-%m-%d",
        "full-date": "%Y-%m-%d",
        "12-hour": "%I:%M %p",
        "24-hour": "%H:%M",
        "datetime": "%Y-%m-%d %H:%M:%S",
    }

    if value is None:
        return "N/A"

    if format_spec in available_formats:
        format_spec = available_formats[format_spec]

    return value.strftime(format_spec)


def currency_formatter(value: int) -> str:
    dollar_amount = convert_cents_to_dollars(value)
    return f"${dollar_amount:.2f}"


def phone_formatter(value: str) -> str:
    return f"({value[:3]})-{value[3:6]}-{value[6:]}"
