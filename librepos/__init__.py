from flask import Flask, redirect, url_for

from librepos.cli.manage import add_cli_commands
from librepos.features import register_features
from librepos.utils.formatters import (
    phone_formatter,
    currency_formatter,
    date_formatter,
    time_formatter,
    un_snake_formatter,
    strip_spaces_formatter,
)


def create_app():
    _template_folder = "ui/templates"
    _static_folder = "ui/static"

    app = Flask(
        __name__, template_folder=_template_folder, static_folder=_static_folder
    )

    app.config.from_pyfile("config.py")

    app.config.from_envvar("LIBREPOS_SETTINGS", silent=True)

    # load extensions
    init_extensions(app)

    # load custom jinja filters
    custom_jinja_filters(app)

    # register features
    register_features(app)

    @app.route("/")
    def index():
        return redirect(url_for("order.list_orders"))

    # load cli commands
    add_cli_commands(app)

    return app


def init_extensions(app):
    from .extensions import db, login_manager, mail, csrf
    from librepos.features.iam.models import User

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "iam.auth.login"  # type: ignore
    login_manager.session_protection = "strong"
    login_manager.refresh_view = "auth.reauthenticate"  # type: ignore
    login_manager.needs_refresh_message = (
        "To protect your account, please reauthenticate to access this page."
    )
    login_manager.needs_refresh_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


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
