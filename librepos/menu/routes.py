from flask import Blueprint, render_template, flash, redirect, url_for, jsonify
from flask_login import login_required

from librepos.utils import sanitize_form_data
from librepos.auth.decorators import permission_required

from .service import MenuService
from .forms import CategoryForm

menu_bp = Blueprint("menu", __name__, template_folder="templates", url_prefix="/menu")

menu_service = MenuService()


@menu_bp.before_request
@login_required
def before_request():
    """Force the user to log in before accessing any page."""
    pass


# ======================================================================================================================
#                                              CATEGORIES ROUTES
# ======================================================================================================================


# ================================
#            CREATE
# ================================
@menu_bp.post("/create-category")
@permission_required("create_menu_category")
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_service.create_menu_category(sanitized_data)
        flash("Category created successfully.", "success")
    return redirect(url_for("menu.list_categories"))


# ================================
#            READ
# ================================
@menu_bp.get("/categories")
@permission_required("list_menu_categories")
def list_categories():
    context = {
        "title": "Categories",
        "categories": menu_service.list_menu_categories(),
        "form": CategoryForm(),
    }
    return render_template("menu/list_categories.html", **context)


@menu_bp.get("/category/<int:category_id>")
@permission_required("get_menu_category")
def get_category(category_id):
    category = menu_service.get_menu_category(category_id)
    context = {
        "title": category.name if category else "Category",
        "back_url": url_for("menu.list_categories"),
        "form": CategoryForm(obj=category),
        "category": menu_service.get_menu_category(category_id),
    }
    return render_template("menu/get_category.html", **context)


# ================================
#            UPDATE
# ================================
@menu_bp.post("/update-category/<int:category_id>")
@permission_required("update_menu_category")
def update_category(category_id):
    form = CategoryForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_service.update_menu_category(category_id, sanitized_data)
        flash("Category updated successfully.", "success")
    return redirect(url_for("menu.get_category", category_id=category_id))


# ================================
#            DELETE
# ================================
@menu_bp.delete("/delete-category/<int:category_id>")
@permission_required("delete_menu_category")
def delete_category(category_id):
    menu_service.delete_menu_category(category_id)
    # Return a redirect header HTMX understands
    response = jsonify(success=True)
    response.headers["HX-Redirect"] = url_for("menu.list_categories")
    return response


# ======================================================================================================================
#                                              GROUPS ROUTES
# ======================================================================================================================


# ================================
#            READ
# ================================
@menu_bp.get("/groups")
def list_groups():
    context = {"title": "Groups", "groups": menu_service.list_menu_groups()}
    return render_template("menu/list_groups.html", **context)


# ======================================================================================================================
#                                              ITEMS ROUTES
# ======================================================================================================================


# ================================
#            READ
# ================================
@menu_bp.get("/items")
def list_items():
    context = {"title": "Items", "items": menu_service.list_menu_items()}
    return render_template("menu/list_items.html", **context)
