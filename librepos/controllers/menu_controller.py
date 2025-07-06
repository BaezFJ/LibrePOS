from flask import Blueprint, render_template, flash, redirect, url_for, jsonify, request
from flask_login import login_required

from librepos.forms import MenuCategoryForm, MenuGroupForm, MenuItemForm
from librepos.services import MenuCategoryService, MenuGroupService, MenuItemService
from librepos.utils import sanitize_form_data
from librepos.utils.decorators import permission_required

menu_bp = Blueprint("menu", __name__, template_folder="templates", url_prefix="/menu")

menu_category_service = MenuCategoryService()
menu_group_service = MenuGroupService()
menu_item_service = MenuItemService()


@menu_bp.before_request
@login_required
def before_request():
    """Force the user to log in before accessing any page."""
    pass


@menu_bp.get("/")
def home():
    """Render the home page."""
    context = {
        "title": "Menu",
        "back_url": url_for("settings.home"),
    }
    return render_template("menu/home.html", **context)


# ======================================================================================================================
#                                              CATEGORIES ROUTES
# ======================================================================================================================


# ================================
#            CREATE
# ================================
@menu_bp.post("/create-category")
@permission_required("menu.create.category")
def create_category():
    form = MenuCategoryForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_category_service.create_category(sanitized_data)
        flash("Category created successfully.", "success")
    return redirect(url_for("menu.list_categories"))


# ================================
#            READ
# ================================
@menu_bp.get("/categories")
@permission_required("menu.list.categories")
def list_categories():
    context = {
        "title": "Categories",
        "back_url": url_for(".home"),
        "categories": menu_category_service.list_categories(),
        "form": MenuCategoryForm(),
    }
    return render_template("menu/list_categories.html", **context)


@menu_bp.get("/category/<int:category_id>")
@permission_required("menu.read.category")
def get_category(category_id):
    category = menu_category_service.get_category_by_id(category_id)
    context = {
        "title": category.name if category else "Category",
        "back_url": url_for("menu.list_categories"),
        "form": MenuCategoryForm(obj=category),
        "category": menu_category_service.get_category_by_id(category_id),
    }
    return render_template("menu/get_category.html", **context)


@menu_bp.get("hx/categories")
def get_hx_categories():
    order_id = request.args.get("order_id")
    categories = menu_category_service.list_active_categories()
    return render_template(
        "menu/hx_categories.html", categories=categories, order_id=order_id
    )


@menu_bp.get("hx/groups/<int:category_id>")
def get_hx_groups(category_id):
    order_id = request.args.get("order_id")
    groups = menu_group_service.list_groups_by_category(category_id)
    category = menu_category_service.get_category_by_id(category_id)
    return render_template(
        "menu/hx_groups.html", groups=groups, category=category, order_id=order_id
    )


@menu_bp.get("hx/group/items/<int:group_id>")
def get_hx_group_items(group_id):
    order_id = request.args.get("order_id")
    group = menu_group_service.get_group_by_id(group_id)
    items = menu_item_service.list_items_by_group(group_id)
    return render_template(
        "menu/hx_group_items.html", items=items, group=group, order_id=order_id
    )


@menu_bp.get("hx/numpad")
def get_hx_numpad():
    order_id = request.args.get("order_id")
    item_id = request.args.get("item_id")
    context = {
        "item_id": item_id,
        "order_id": order_id,
    }
    return render_template("menu/hx_numpad.html", **context)


# ================================
#            UPDATE
# ================================
@menu_bp.post("/update-category/<int:category_id>")
@permission_required("menu.update.category")
def update_category(category_id):
    form = MenuCategoryForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_category_service.update_category(category_id, sanitized_data)
    return redirect(url_for("menu.get_category", category_id=category_id))


# ================================
#            DELETE
# ================================
@menu_bp.post("/delete-category/<int:category_id>")
@permission_required("menu.delete.category")
def delete_category(category_id):
    _category = menu_category_service.get_category_by_id(category_id)
    menu_category_service.delete_category(category_id)
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
@permission_required("menu.create.group")
def create_group():
    form = MenuGroupForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_group_service.create_group(sanitized_data)
    return redirect(url_for("menu.list_groups"))


# ================================
#            READ
# ================================
@menu_bp.get("/groups")
@permission_required("menu.list.groups")
def list_groups():
    form = MenuGroupForm()
    context = {
        "title": "Groups",
        "back_url": url_for(".home"),
        "groups": menu_group_service.list_groups(),
        "form": form,
    }
    return render_template("menu/list_groups.html", **context)


@menu_bp.get("/group/<int:group_id>")
@permission_required("menu.read.group")
def get_group(group_id):
    group = menu_group_service.get_group_by_id(group_id)
    form = MenuGroupForm(obj=group)
    context = {
        "title": group.name if group else "Group",
        "back_url": url_for("menu.list_groups"),
        "group": group,
        "form": form,
    }
    return render_template("menu/get_group.html", **context)


# ================================
#            UPDATE
# ================================
@menu_bp.post("/update-group/<int:group_id>")
@permission_required("menu.update.group")
def update_group(group_id):
    form = MenuGroupForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_group_service.update_group(group_id, sanitized_data)
    return redirect(url_for("menu.get_group", group_id=group_id))


# ================================
#            DELETE
# ================================
@menu_bp.post("/delete-group/<int:group_id>")
@permission_required("menu.delete.group")
def delete_group(group_id):
    menu_group_service.delete_group(group_id)
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
@permission_required("menu.create.item")
def create_item():
    form = MenuItemForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_item_service.create_menu_item(sanitized_data)
    return redirect(url_for("menu.list_items"))


# ================================
#            READ
# ================================
@menu_bp.get("/items")
@permission_required("menu.list.items")
def list_items():
    form = MenuItemForm()
    context = {
        "title": "Items",
        "back_url": url_for(".home"),
        "items": menu_item_service.list_menu_items(),
        "form": form,
    }
    return render_template("menu/list_items.html", **context)


@menu_bp.get("/item/<int:item_id>")
@permission_required("menu.read.item")
def get_item(item_id):
    item = menu_item_service.get_item_by_id(item_id)
    form = MenuItemForm(obj=item)
    context = {
        "title": item.name if item else "Item",
        "back_url": url_for("menu.list_items"),
        "item": item,
        "form": form,
    }
    return render_template("menu/get_item.html", **context)


# ================================
#            UPDATE
# ================================
@menu_bp.post("/update-item/<int:item_id>")
@permission_required("menu.update.item")
def update_item(item_id):
    form = MenuItemForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_item_service.update_menu_item(item_id, sanitized_data)
    return redirect(url_for("menu.get_item", item_id=item_id))


# ================================
#            DELETE
# ================================
@menu_bp.post("/delete-item/<int:item_id>")
@permission_required("menu.delete.item")
def delete_item(item_id):
    menu_item_service.delete_menu_item(item_id)
    response = jsonify(success=True)
    response.headers["HX-Redirect"] = url_for("menu.list_items")
    return response
