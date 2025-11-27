import os
from importlib.metadata import version
from pathlib import Path

from flask import Flask
from jinja2 import FileSystemBytecodeCache, StrictUndefined, DebugUndefined

from librepos.cli import add_cli_commands
from librepos.features.urls import urlpatterns
from librepos.utils.jinja import custom_jinja_filters
from .extensions import init_extensions


def create_app(config: str | type | None = None):
    _template_dir = "../ui/templates"
    _static_dir = "../ui/static"

    app = Flask(__name__, template_folder=_template_dir, static_folder=_static_dir)

    from .config import CONFIG_BY_NAME, DevelopmentConfig, BaseConfig

    cfg = config
    if cfg is None:
        cfg = os.getenv("FLASK_ENV", "development").lower()

    if isinstance(cfg, str):
        config_cls = CONFIG_BY_NAME.get(cfg.lower(), DevelopmentConfig)
    elif isinstance(cfg, type) and issubclass(cfg, BaseConfig):
        config_cls = cfg
    else:
        config_cls = DevelopmentConfig

    app.config.from_object(config_cls)
    config_cls.validate()

    # Catch missing variables early in development.
    app.jinja_env.undefined = StrictUndefined if app.config["DEBUG"] else DebugUndefined

    # # Nicer whitespace handling (optional)
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    # jinja cache
    def ensure_jinja_cache_dir():
        cache_dir = Path("instance/jinja_cache")
        cache_dir.mkdir(parents=True, exist_ok=True)

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

    # register features and core routes
    urlpatterns(app)

    # load cli_2 commands
    add_cli_commands(app)

    return app
