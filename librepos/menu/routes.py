from flask import Blueprint, render_template
from flask_login import login_required

from .service import MenuService

menu_bp = Blueprint("menu", __name__, template_folder="templates", url_prefix="/menu")

menu_service = MenuService()


@menu_bp.before_request
@login_required
def before_request():
    """Force the user to log in before accessing any page."""
    pass


@menu_bp.get("/categories")
def list_categories():
    context = {"title": "Categories", "categories": menu_service.list_menu_categories()}
    return render_template("menu/list_categories.html", **context)


@menu_bp.get("/groups")
def list_groups():
    context = {"title": "Groups", "groups": menu_service.list_menu_groups()}
    return render_template("menu/list_groups.html", **context)


@menu_bp.get("/items")
def list_items():
    context = {"title": "Items", "items": menu_service.list_menu_items()}
    return render_template("menu/list_items.html", **context)
