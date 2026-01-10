"""Route handlers for menu blueprint."""

from flask import flash, redirect, render_template, url_for

from . import bp
from .models import Category
from .services import CategoryService

sidenav_title = {"sidenav_title": "Menu"}


@bp.route("/")
def index():
    """List view for a menu."""
    context = {
        "head_title": "Menu | LibrePOS",
        "nav_title": "Dashboard",
        **sidenav_title,
    }
    return render_template("menu/index.html", **context)


@bp.route("/items")
def items():
    """List view for menu items."""
    context = {
        "head_title": "Menu Items | LibrePOS",
        "nav_title": "Items",
        **sidenav_title,
    }
    return render_template("menu/items.html", **context)


@bp.route("/items/<int:item_id>")
def item_detail(item_id):
    """Detail view for a single menu item."""
    context = {
        "head_title": f"Item #{item_id} | LibrePOS",
        "nav_title": "Item Detail",
        "item_id": item_id,
        **sidenav_title,
    }
    return render_template("menu/item_detail.html", **context)


@bp.route("/categories")
def categories():
    """List view for menu categories"""
    _categories = Category.get_all()
    context = {
        "head_title": "Menu Categories | LibrePOS",
        "nav_title": "Categories",
        "categories": _categories,
        **sidenav_title,
    }
    return render_template("menu/categories.html", **context)


@bp.route("/category/<int:category_id>")
def category_detail(category_id):
    """Detail view for a single menu category."""
    _category = Category.get_by_id(category_id)
    if not _category:
        flash("Category not found", "error")
        return redirect(url_for("menu.categories"))

    context = {
        "head_title": f"{_category.name} | Categories | LibrePOS",
        "nav_title": _category.name,
        **sidenav_title,
    }
    return render_template("menu/category_detail.html", **context)


@bp.route("/category/<int:cat_id>/delete", methods=["POST"])
def category_delete(cat_id):
    """Delete a category."""
    _category = Category.get_by_id(cat_id)
    if not _category:
        flash("Category not found", "error")
        return redirect(url_for("menu.categories"))

    category_name = _category.name
    CategoryService.delete(cat_id)
    flash(f"Category '{category_name}' deleted successfully", "success")
    return redirect(url_for("menu.categories"))


@bp.route("/modifiers")
def modifiers():
    """List view for menu modifiers"""
    context = {
        "head_title": "Menu Modifiers | LibrePOS",
        "nav_title": "Modifiers",
        **sidenav_title,
    }
    return render_template("menu/modifiers.html", **context)


@bp.route("/modifier-groups")
def modifier_groups():
    """List view for menu modifier groups"""
    context = {
        "head_title": "Menu Modifier Groups | LibrePOS",
        "nav_title": "Modifier Groups",
        **sidenav_title,
    }
    return render_template("menu/modifier_groups.html", **context)


@bp.route("/menus")
def menus():
    """List view for menu menus"""
    context = {
        "head_title": "Menu Menus | LibrePOS",
        "nav_title": "Menus",
        **sidenav_title,
    }
    return render_template("menu/menus.html", **context)


@bp.route("/pricing")
def pricing():
    """List view for menu pricing rules"""
    context = {
        "head_title": "Menu Pricing | LibrePOS",
        "nav_title": "Pricing",
        **sidenav_title,
    }
    return render_template("menu/pricing.html", **context)


@bp.route("/tags")
def tags():
    """List view for menu tags"""
    context = {
        "head_title": "Menu Tags | LibrePOS",
        "nav_title": "Tags",
        **sidenav_title,
    }
    return render_template("menu/tags.html", **context)


@bp.route("/settings")
def settings():
    """List view for menu settings"""
    context = {
        "head_title": "Menu Settings | LibrePOS",
        "nav_title": "Settings",
        **sidenav_title,
    }
    return render_template("menu/settings.html", **context)
