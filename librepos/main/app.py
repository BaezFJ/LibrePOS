import os
from importlib.metadata import version

from flask import Flask
from jinja2 import FileSystemBytecodeCache, StrictUndefined, DebugUndefined

from librepos.cli import add_cli_commands
from librepos.utils.jinja import custom_jinja_filters
from librepos.features.urls import urlpatterns

from .extensions import init_extensions


def create_app():
    _template_dir = "../ui/templates"
    _static_dir = "../ui/static"

    app = Flask(__name__, template_folder=_template_dir, static_folder=_static_dir)

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

    # register features and main routes
    urlpatterns(app)

    # load cli_2 commands
    add_cli_commands(app)

    return app
