from .formatters import (
    date_formatter,
    time_formatter,
    currency_formatter,
    phone_formatter,
    un_snake_formatter,
    strip_spaces_formatter,
)


def custom_jinja_filters(app):
    @app.template_filter("date")
    def format_date(value):
        return date_formatter(value)

    @app.template_filter("time")
    def format_time(value):
        return time_formatter(value)

    @app.template_filter("currency")
    def format_currency(value):
        return currency_formatter(value)

    @app.template_filter("phone")
    def format_phone(value):
        return phone_formatter(value)

    @app.template_filter("un_snake")
    def format_un_snake(value):
        return un_snake_formatter(value)

    @app.template_filter("strip_spaces")
    def format_strip_spaces(value):
        return strip_spaces_formatter(value)
