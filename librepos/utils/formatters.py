import re
from datetime import datetime

from babel.numbers import get_currency_symbol
from flask import current_app

from .financial import convert_cents_to_dollars


def receipt_number_formatter(prefix: str, counter: int, suffix: str = "") -> str:
    prefix = f"{prefix:02d}"
    number_part = f"{counter:04d}"
    return f"{prefix}-{number_part}{suffix}" if suffix else f"{prefix}-{number_part}"


def date_formatter(value: datetime | None) -> str:
    if value is None:
        return "N/A"
    system_date_format = current_app.config["DATE_FORMAT"]
    return value.strftime(system_date_format)


def time_formatter(value: datetime | None) -> str:
    if value is None:
        return "N/A"
    system_time_format = current_app.config["TIME_FORMAT"]
    return value.strftime(system_time_format)


def currency_formatter(value: int) -> str:
    dollar_amount = convert_cents_to_dollars(value)
    currency_code = current_app.config["CURRENCY"]
    locale = current_app.config["BABEL_DEFAULT_LOCALE"]
    currency_symbol = get_currency_symbol(currency_code, locale=locale)
    return f"{currency_symbol} {dollar_amount:.2f}"


def phone_formatter(value: str) -> str:
    if value is None:
        return "N/A"
    return f"({value[:3]}) {value[3:6]}-{value[6:]}"


def un_snake_formatter(value: str) -> str:
    if value is None:
        return "N/A"
    value = value.replace("_", " ")
    return value


def strip_spaces_formatter(value):
    return re.sub(r"\s+", "", value)
