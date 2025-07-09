from flask import Blueprint, render_template, flash, redirect, url_for, jsonify, request

from librepos.utils import sanitize_form_data
from librepos.utils.decorators import permission_required
from ..forms import MenuCategoryForm
from ..services import MenuCategoryService, MenuGroupService, MenuItemService

category_bp = Blueprint("category", __name__, template_folder="templates", url_prefix="/category")

menu_category_service = MenuCategoryService()
menu_group_service = MenuGroupService()
menu_item_service = MenuItemService()


# ================================
#            CREATE
# ================================
@category_bp.post("/create")
@permission_required("menu.create.category")
def create_category():
    form = MenuCategoryForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_category_service.create_category(sanitized_data)
        flash("Category created successfully.", "success")
    return redirect(url_for("menu.category.list_categories"))


# ================================
#            READ
# ================================
@category_bp.get("/")
@permission_required("menu.list.category")
def list_categories():
    context = {
        "title": "Categories",
        "back_url": url_for("menu.home"),
        "category": menu_category_service.list_categories(),
        "form": MenuCategoryForm(),
    }
    return render_template("menu/category/list_categories.html", **context)


@category_bp.get("/<int:category_id>")
@permission_required("menu.read.category")
def get_category(category_id):
    category = menu_category_service.get_category_by_id(category_id)
    context = {
        "title": category.name if category else "Category",
        "back_url": url_for("menu.category.list_categories"),
        "form": MenuCategoryForm(obj=category),
        "category": menu_category_service.get_category_by_id(category_id),
    }
    return render_template("menu/category/get_category.html", **context)


# TODO 7/9/25 : Relocate route to orders feature as it handles order-related loading
@category_bp.get("hx/categories")
def get_hx_categories():
    order_id = request.args.get("order_id")
    categories = menu_category_service.list_active_categories()
    return render_template(
        "menu/category/hx_categories.html", categories=categories, order_id=order_id
    )


# TODO 7/9/25 : Relocate route to orders feature as it handles order-related loading
@category_bp.get("hx/groups/<int:category_id>")
def get_hx_groups(category_id):
    order_id = request.args.get("order_id")
    groups = menu_group_service.list_groups_by_category(category_id)
    category = menu_category_service.get_category_by_id(category_id)
    return render_template(
        "menu/group/hx_groups.html", groups=groups, category=category, order_id=order_id
    )


# TODO 7/9/25 : Relocate route to orders feature as it handles order-related loading
@category_bp.get("hx/group/items/<int:group_id>")
def get_hx_group_items(group_id):
    order_id = request.args.get("order_id")
    group = menu_group_service.get_group_by_id(group_id)
    items = menu_item_service.list_items_by_group(group_id)
    return render_template(
        "menu/item/hx_group_items.html", items=items, group=group, order_id=order_id
    )


# TODO 7/9/25 : Relocate route to orders feature as it handles order-related loading
@category_bp.get("hx/numpad")
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
@category_bp.post("/<int:category_id>/update")
@permission_required("menu.update.category")
def update_category(category_id):
    form = MenuCategoryForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_category_service.update_category(category_id, sanitized_data)
    return redirect(url_for("menu.category.get_category", category_id=category_id))


# ================================
#            DELETE
# ================================
@category_bp.post("/<int:category_id>/delete")
@permission_required("menu.delete.category")
def delete_category(category_id):
    menu_category_service.delete_category(category_id)
    # Return a redirect header HTMX understands
    response = jsonify(success=True)
    response.headers["HX-Redirect"] = url_for("menu.category.list_categories")
    return response
