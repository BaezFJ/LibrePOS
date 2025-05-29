from flask import Flask

from .manage import add_cli_commands
from .router import register_blueprints
from .utils.formatters import datetime_formatter, phone_formatter, currency_formatter


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

    # register blueprints
    register_blueprints(app)

    # load cli commands
    add_cli_commands(app)

    return app


def init_extensions(app):
    from .extensions import db, login_manager, mail, csrf
    from librepos.models.users import User

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"  # type: ignore
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
    @app.template_filter("datetime")
    def format_date(value, format_spec="short-date"):
        return datetime_formatter(value, format_spec)

    @app.template_filter("currency")
    def format_currency(value):
        return currency_formatter(value)

    @app.template_filter("phone")
    def format_phone(value):
        return phone_formatter(value)
