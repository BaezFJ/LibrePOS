"""
Menu management
"""

from flask import Blueprint

bp = Blueprint(
    "menu",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/menu/static",
    url_prefix="/menu",
)

from . import models, routes  # noqa: E402  # pyright: ignore[reportUnusedImport]
