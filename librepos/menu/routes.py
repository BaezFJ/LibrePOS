from flask import Blueprint, render_template, flash, redirect, url_for, jsonify
from flask_login import login_required

from librepos.utils import sanitize_form_data
from librepos.auth.decorators import permission_required

from .service import MenuService
from .forms import CategoryForm, GroupForm, MenuItemForm

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


@menu_bp.get("hx/categories")
def get_hx_categories():
    categories = menu_service.get_active_menu_categories()
    return render_template("menu/hx_categories.html", categories=categories)


@menu_bp.get("hx/groups/<int:category_id>")
def get_hx_groups(category_id):
    groups = menu_service.get_menu_category_groups(category_id)
    category = menu_service.get_menu_category(category_id)
    return render_template("menu/htmx_groups.html", groups=groups, category=category)


@menu_bp.get("hx/items/<int:group_id>")
def get_hx_items(group_id):
    group = menu_service.get_menu_group(group_id)
    items = menu_service.list_group_menu_items(group_id)
    return render_template("menu/htmx_items.html", items=items, group=group)


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
@menu_bp.post("/delete-category/<int:category_id>")
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
#            CREATE
# ================================
@menu_bp.post("/create-group")
@permission_required("create_menu_group")
def create_group():
    form = GroupForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_service.create_menu_group(sanitized_data)
        flash("Group created successfully.", "success")
    return redirect(url_for("menu.list_groups"))


# ================================
#            READ
# ================================
@menu_bp.get("/groups")
@permission_required("list_menu_groups")
def list_groups():
    form = GroupForm()
    context = {
        "title": "Groups",
        "groups": menu_service.list_menu_groups(),
        "form": form,
    }
    return render_template("menu/list_groups.html", **context)


@menu_bp.get("/group/<int:group_id>")
@permission_required("get_menu_group")
def get_group(group_id):
    group = menu_service.get_menu_group(group_id)
    form = GroupForm(obj=group)
    context = {
        "title": group.name if group else "Group",
        "back_url": url_for("menu.list_groups"),
        "group": menu_service.get_menu_group(group_id),
        "form": form,
    }
    return render_template("menu/get_group.html", **context)


# ================================
#            UPDATE
# ================================
@menu_bp.post("/update-group/<int:group_id>")
@permission_required("update_menu_group")
def update_group(group_id):
    form = GroupForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_service.update_menu_group(group_id, sanitized_data)
        flash("Group updated successfully.", "success")
    return redirect(url_for("menu.get_group", group_id=group_id))


# ================================
#            DELETE
# ================================
@menu_bp.post("/delete-group/<int:group_id>")
@permission_required("delete_menu_group")
def delete_group(group_id):
    menu_service.delete_menu_group(group_id)
    response = jsonify(success=True)
    response.headers["HX-Redirect"] = url_for("menu.list_groups")
    return response


# ======================================================================================================================
#                                              ITEMS ROUTES
# ======================================================================================================================


# ================================
#            CREATE
# ================================
@menu_bp.post("/create-item")
@permission_required("create_menu_item")
def create_item():
    form = MenuItemForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_service.create_menu_item(sanitized_data)
        flash("Item created successfully.", "success")
    return redirect(url_for("menu.list_items"))


# ================================
#            READ
# ================================
@menu_bp.get("/items")
@permission_required("list_menu_items")
def list_items():
    form = MenuItemForm()
    context = {"title": "Items", "items": menu_service.list_menu_items(), "form": form}
    return render_template("menu/list_items.html", **context)


@menu_bp.get("/item/<int:item_id>")
@permission_required("get_menu_item")
def get_item(item_id):
    item = menu_service.get_menu_item(item_id)
    form = MenuItemForm(obj=item)
    context = {
        "title": item.name if item else "Item",
        "back_url": url_for("menu.list_items"),
        "item": menu_service.get_menu_item(item_id),
        "form": form,
    }
    return render_template("menu/get_item.html", **context)


# ================================
#            UPDATE
# ================================
@menu_bp.post("/update-item/<int:item_id>")
@permission_required("update_menu_item")
def update_item(item_id):
    form = MenuItemForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_service.update_menu_item(item_id, sanitized_data)
        flash("Item updated successfully.", "success")
    return redirect(url_for("menu.get_item", item_id=item_id))


# ================================
#            DELETE
# ================================
@menu_bp.post("/delete-item/<int:item_id>")
@permission_required("delete_menu_item")
def delete_item(item_id):
    menu_service.delete_menu_item(item_id)
    response = jsonify(success=True)
    response.headers["HX-Redirect"] = url_for("menu.list_items")
    return response
