from flask import Flask

from .manage import add_cli_commands
from .router import register_blueprints
from .utils import convert_cents_to_dollars


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
    datetime_formats = {
        "short-date": "%y-%m-%d",
        "full-date": "%Y-%m-%d",
        "time": "%I:%M %p",
        "time-24": "%H:%M",
        "datetime": "%Y-%m-%d %H:%M:%S",
    }
    default_datetime_format = "full-date"

    @app.template_filter("datetime")
    def format_datetime(value, format_spec=default_datetime_format):
        if value is None:
            return "N/A"
        if format_spec in datetime_formats:
            format_spec = datetime_formats[format_spec]
        return value.strftime(format_spec)

    @app.template_filter("currency")
    def format_currency(value):
        value = convert_cents_to_dollars(value)
        return f"${value:.2f}"

    @app.template_filter("phone")
    def format_phone(value):
        return f"({value[:3]}) {value[3:6]}-{value[6:]}"
