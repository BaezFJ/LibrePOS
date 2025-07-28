from flask import Blueprint, render_template, redirect, url_for, request

from librepos.common.forms import ConfirmationForm
from librepos.utils import sanitize_form_data
from librepos.utils.decorators import permission_required
from ..forms import MenuCategoryForm
from ..services import MenuCategoryService, MenuGroupService, MenuItemService
from ..utils.enums import MenuPermissions

category_bp = Blueprint(
    "category", __name__, template_folder="templates", url_prefix="/category"
)

menu_category_service = MenuCategoryService()
menu_group_service = MenuGroupService()
menu_item_service = MenuItemService()


# ================================
#            CREATE
# ================================
@category_bp.route("/create", methods=["POST", "GET"])
@permission_required(MenuPermissions.CREATE_CATEGORY)
def create_category():
    """Display & process the creation category page."""
    form = MenuCategoryForm()
    context = {
        "title": "MenuCategory",
        "back_url": url_for(".list_categories"),
        "form": form,
    }
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        new_category = menu_category_service.create_category(sanitized_data)
        if new_category:
            return redirect(
                url_for("menu.category.get_category", category_id=new_category.id)
            )
    return render_template("menu/category/create_category.html", **context)


# ================================
#            READ
# ================================
@category_bp.get("/")
@permission_required(MenuPermissions.LIST_CATEGORY)
def list_categories():
    context = {
        "title": "Categories",
        "back_url": url_for("menu.home"),
        "categories": menu_category_service.repository.get_all(),
        "form": MenuCategoryForm(),
    }
    return render_template("menu/category/list_categories.html", **context)


@category_bp.get("/<int:category_id>")
@permission_required(MenuPermissions.READ_CATEGORY)
def get_category(category_id):
    context = {
        "title": "MenuCategory",
        "back_url": url_for("menu.category.list_categories"),
        "form": ConfirmationForm(),
        "category": menu_category_service.repository.get_by_id(category_id),
    }
    return render_template("menu/category/get_category.html", **context)


# TODO 7/9/25 : Relocate route to orders feature as it handles order-related loading
@category_bp.get("hx/categories")
def get_hx_categories():
    order_id = request.args.get("order_id")
    categories = menu_category_service.repository.get_active_categories()
    return render_template(
        "menu/category/hx_categories.html", categories=categories, order_id=order_id
    )


# TODO 7/9/25 : Relocate route to orders feature as it handles order-related loading
@category_bp.get("hx/groups/<int:category_id>")
def get_hx_groups(category_id):
    order_id = request.args.get("order_id")
    groups = menu_group_service.repository.list_groups_by_category(category_id)
    category = menu_category_service.repository.get_by_id(category_id)
    return render_template(
        "menu/group/hx_groups.html", groups=groups, category=category, order_id=order_id
    )


# TODO 7/9/25 : Relocate route to orders feature as it handles order-related loading
@category_bp.get("hx/group/items/<int:group_id>")
def get_hx_group_items(group_id):
    order_id = request.args.get("order_id")
    group = menu_group_service.repository.get_by_id(group_id)
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
@category_bp.route("/<int:category_id>/update", methods=["POST", "GET"])
@permission_required(MenuPermissions.UPDATE_CATEGORY)
def update_category(category_id):
    """Display & process the update category page."""
    category = menu_category_service.repository.get_by_id(category_id)
    form = MenuCategoryForm(obj=category, submit_text="Update")
    context = {
        "title": "Update",
        "back_url": url_for(".get_category", category_id=category_id),
        "form": form,
        "category": category,
    }
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_category_service.update_category(category_id, sanitized_data)
        return redirect(url_for(".get_category", category_id=category_id))
    return render_template("menu/category/update_category.html", **context)


# ================================
#            DELETE
# ================================
@category_bp.post("/<int:category_id>/delete")
@permission_required(MenuPermissions.DELETE_CATEGORY)
def delete_category(category_id):
    form = ConfirmationForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        if menu_category_service.delete_category(sanitized_data, category_id):
            return redirect(url_for(".list_categories"))
        return redirect(url_for(".get_category", category_id=category_id))
    return redirect(url_for(".list_categories"))
