import re
from datetime import datetime

from babel.numbers import get_currency_symbol

from librepos.features.settings.repositories import SystemSettingsRepository
from .financial import convert_cents_to_dollars

system_settings_repo = SystemSettingsRepository()


def receipt_number_formatter(prefix: str, counter: int, suffix: str = "") -> str:
    prefix = f"{prefix:02d}"
    number_part = f"{counter:04d}"
    return f"{prefix}-{number_part}{suffix}" if suffix else f"{prefix}-{number_part}"


def date_formatter(value: datetime | None) -> str:
    if value is None:
        return "N/A"
    system_date_format = system_settings_repo.get_date_format()
    return value.strftime(system_date_format)


def time_formatter(value: datetime | None) -> str:
    if value is None:
        return "N/A"
    system_time_format = system_settings_repo.get_time_format()
    return value.strftime(system_time_format)


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
    currency_code = system_settings_repo.get_currency()
    locale = system_settings_repo.get_locale()
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


def name_formatter(value: str) -> str:
    if value is None:
        return "N/A"
    return strip_spaces_formatter(un_snake_formatter(value).title())
