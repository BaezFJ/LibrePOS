from flask import Blueprint, render_template, redirect, url_for, jsonify

from librepos.utils import sanitize_form_data
from librepos.utils.decorators import permission_required
from ..forms import MenuItemForm
from ..services import MenuItemService

item_bp = Blueprint("item", __name__, template_folder="templates", url_prefix="/items")

menu_item_service = MenuItemService()


# ================================
#            CREATE
# ================================
@item_bp.post("/create")
@permission_required("menu.create.item")
def create_item():
    form = MenuItemForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_item_service.create_menu_item(sanitized_data)
    return redirect(url_for("menu.item.list_items"))


# ================================
#            READ
# ================================
@item_bp.get("/")
@permission_required("menu.list.items")
def list_items():
    form = MenuItemForm()
    context = {
        "title": "Items",
        "back_url": url_for("menu.home"),
        "items": menu_item_service.list_menu_items(),
        "form": form,
    }
    return render_template("menu/item/list_items.html", **context)


@item_bp.get("/<int:item_id>")
@permission_required("menu.read.item")
def get_item(item_id):
    item = menu_item_service.get_item_by_id(item_id)
    form = MenuItemForm(obj=item)
    context = {
        "title": item.name if item else "Item",
        "back_url": url_for("menu.item.list_items"),
        "item": item,
        "form": form,
    }
    return render_template("menu/item/get_item.html", **context)


# ================================
#            UPDATE
# ================================
@item_bp.post("/<int:item_id>/update")
@permission_required("menu.update.item")
def update_item(item_id):
    form = MenuItemForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_item_service.update_menu_item(item_id, sanitized_data)
    return redirect(url_for("menu.item.get_item", item_id=item_id))


# ================================
#            DELETE
# ================================
@item_bp.post("/<int:item_id>/delete")
@permission_required("menu.delete.item")
def delete_item(item_id):
    menu_item_service.delete_menu_item(item_id)
    response = jsonify(success=True)
    response.headers["HX-Redirect"] = url_for("menu.item.list_items")
    return response
