from flask import Blueprint, render_template, redirect, url_for

from librepos.common.forms import ConfirmationForm
from librepos.utils import sanitize_form_data
from librepos.utils.decorators import permission_required
from ..forms import MenuItemForm
from ..services import MenuItemService

item_bp = Blueprint("item", __name__, template_folder="templates", url_prefix="/items")

menu_item_service = MenuItemService()


# ================================
#            CREATE
# ================================
@item_bp.route("/create", methods=["POST", "GET"])
@permission_required("menu.create.item")
def create_item():
    form = MenuItemForm()
    context = {
        "title": "Item",
        "back_url": url_for(".list_items"),
        "form": form,
    }
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        new_item = menu_item_service.create_item(sanitized_data)
        if new_item:
            return redirect(url_for(".get_item", item_id=new_item.id))
    return render_template("menu/item/create_item.html", **context)


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
    context = {
        "title": "Item",
        "back_url": url_for(".list_items"),
        "item": menu_item_service.get_item_by_id(item_id),
        "form": ConfirmationForm(),
    }
    return render_template("menu/item/get_item.html", **context)


# ================================
#            UPDATE
# ================================
@item_bp.route("/<int:item_id>/update", methods=["POST", "GET"])
@permission_required("menu.update.item")
def update_item(item_id):
    item = menu_item_service.get_item_by_id(item_id)
    form = MenuItemForm(obj=item, submit_text="Update")
    context = {
        "title": "Update",
        "back_url": url_for(".get_item", item_id=item_id),
        "form": form,
        "item": item,
    }
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_item_service.update_item(item_id, sanitized_data)
        return redirect(url_for(".get_item", item_id=item_id))
    return render_template("menu/item/update_item.html", **context)


# ================================
#            DELETE
# ================================
@item_bp.post("/<int:item_id>/delete")
@permission_required("menu.delete.item")
def delete_item(item_id):
    form = ConfirmationForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        if menu_item_service.delete_item(sanitized_data, item_id):
            return redirect(url_for(".list_items"))
        return redirect(url_for(".get_item", item_id=item_id))
    return redirect(url_for(".list_items"))
