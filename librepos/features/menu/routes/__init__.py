from flask import Blueprint, render_template, url_for

from librepos.utils.decorators import permission_required
from .category_routes import category_bp
from .group_routes import group_bp
from .item_routes import item_bp

menu_bp = Blueprint(
    "menu", __name__, template_folder="../templates", url_prefix="/menu"
)

# Subroutes
menu_bp.register_blueprint(category_bp)
menu_bp.register_blueprint(group_bp)
menu_bp.register_blueprint(item_bp)


@menu_bp.get("/")
@permission_required("menu.access")
def home():
    """Render the home page."""
    context = {
        "title": "Menu",
        "back_url": url_for("settings.home"),
    }
    return render_template("menu/home.html", **context)
