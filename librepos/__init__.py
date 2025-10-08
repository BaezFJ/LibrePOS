import os
from importlib.metadata import version

from flask import Flask
from jinja2 import StrictUndefined, DebugUndefined, FileSystemBytecodeCache

from librepos.cli.manage import add_cli_commands
from librepos.features.routes import urlpatterns
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

    # Catch missing variables early in development.
    app.jinja_env.undefined = StrictUndefined if app.config["DEBUG"] else DebugUndefined

    # # Nicer whitespace handling (optional)
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    # jinja cache
    def ensure_jinja_cache_dir():
        cache_dir = "instance/jinja_cache"
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    # Ensure the cache directory exists
    ensure_jinja_cache_dir()

    # Bytecode cache (big templates render faster after the first hit)
    app.jinja_env.bytecode_cache = FileSystemBytecodeCache(
        directory="instance/jinja_cache", pattern="%s.cache"
    )

    @app.context_processor
    def inject_global_variables():
        librepos_version = version("librepos")
        business_name = app.config.get("BUSINESS_NAME") or "LibrePOS"
        return dict(app_version=librepos_version, business_name=business_name)

    # load extensions
    init_extensions(app)

    # load custom jinja filters
    custom_jinja_filters(app)

    # register features
    urlpatterns(app)

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

    login_manager.login_view = "iam.auth.get_login"  # type: ignore
    login_manager.session_protection = "strong"
    # login_manager.refresh_view = "auth.reauthenticate"  # type: ignore
    # login_manager.needs_refresh_message = (
    #     "To protect your account, please reauthenticate to access this page."
    # )
    # login_manager.needs_refresh_message_category = "info"

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
