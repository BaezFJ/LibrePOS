import os
from importlib.metadata import version
from pathlib import Path

from flask import Flask, render_template, send_from_directory
from jinja2 import DebugUndefined, FileSystemBytecodeCache, StrictUndefined

from librepos.app.blueprints import register_blueprints
from librepos.app.cli import register_cli
from librepos.app.extensions import init_extensions

from .config import CONFIG_BY_NAME, BaseConfig, DevelopmentConfig


def create_app(app_config: str | type | None = None):
    app = Flask(__name__)

    cfg = app_config
    if cfg is None:
        cfg = os.getenv("FLASK_ENV", "development").lower()

    if isinstance(cfg, str):
        config_cls = CONFIG_BY_NAME.get(cfg.lower(), DevelopmentConfig)
    elif isinstance(cfg, type) and issubclass(cfg, BaseConfig):
        config_cls = cfg
    else:
        config_cls = DevelopmentConfig

    settings = config_cls()
    app.config.from_mapping(settings.model_dump())
    config_cls.init_app()

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
        return {"app_version": librepos_version, "business_name": business_name}

    # load extensions
    init_extensions(app)

    @app.get("/")
    def welcome_view():
        return render_template("welcome.html", title="Welcome")

    @app.get("/admin")
    def admin_view():
        return render_template("layouts/admin.html", title="Admin")

    # PWA Routes - serve at root scope for full service worker control
    @app.get("/sw.js")
    def service_worker():
        """Serve service worker from root scope for full PWA control."""
        static_folder = app.static_folder
        if static_folder is None:
            return "Static folder not configured", 500
        response = send_from_directory(
            static_folder,
            "js/sw.js",
            mimetype="application/javascript",
        )
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Service-Worker-Allowed"] = "/"
        return response

    @app.get("/offline.html")
    def offline_page():
        """Serve offline page for service worker fallback."""
        return render_template("offline.html")

    # Register blueprints
    register_blueprints(app)

    # Register CLI commands
    register_cli(app)

    return app
