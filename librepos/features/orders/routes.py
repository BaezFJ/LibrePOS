from flask import Blueprint, render_template, url_for, jsonify, request, redirect
from flask_login import current_user

from librepos.features.menu.services import MenuCategoryService, MenuItemService
from librepos.utils.decorators import permission_required
from .services import OrderService
from .utils.enums import OrderPermissions, OrderStatus

order_bp = Blueprint(
    "order", __name__, template_folder="templates", url_prefix="/orders"
)

order_service = OrderService()
# order_item_service = OrderItemService()
menu_category_service = MenuCategoryService()
menu_item_service = MenuItemService()


# ================================
#            CREATE
# ================================
@order_bp.post("/create-order")
@permission_required(OrderPermissions.CREATE_TICKET)
def create_order():
    new_order = order_service.create_order(data={"user_id": current_user.id})
    response = jsonify(success=True)
    response.headers["HX-Redirect"] = url_for("order.get_order", order_id=new_order.id)
    return response


# ================================
#            READ
# ================================
@order_bp.get("/")
@permission_required(OrderPermissions.LIST_TICKET)
def list_orders():
    context = {
        "title": "Orders",
        "orders": order_service.list_user_pending_orders(current_user.id),
    }
    return render_template("order/list_orders.html", **context)


@order_bp.get("/<int:order_id>")
@permission_required(OrderPermissions.READ_TICKET)
def get_order(order_id):
    order = order_service.order_repo.get_by_id(order_id)
    menu_categories = menu_category_service.repository.get_all()
    context = {
        "title": str(order.order_number) if order else "Order",
        "back_url": url_for("order.list_orders"),
        "sidenav": {"template": "order/_sidenav.html", "icon": "shopping_cart"},
        "order": order,
        "menu_categories": menu_categories,
    }
    return render_template("order/get_order.html", **context)


# ================================
#            UPDATE
# ================================
@order_bp.post("/void-order/<int:order_id>")
@permission_required(OrderPermissions.CREATE_TICKET)
def void_order(order_id):
    order_service.patch_order_status(order_id, OrderStatus.VOIDED)
    response = jsonify(success=True)
    response.headers["HX-Redirect"] = url_for("order.list_orders")
    return response


@order_bp.post("/add-item-to-order")
@permission_required(OrderPermissions.CREATE_TICKET_ITEM)
def add_item_to_order():
    order_id = request.form.get("order_id", type=int, default=0)
    # item_id = request.form.get("item_id", type=int, default=0)
    # quantity = request.form.get("quantity", type=int, default=1)

    # item = menu_item_service.get_item_by_id(item_id)
    # price = item.price if item else 0

    # order_item_service.add_item_to_order(order_id, item_id, quantity, price)
    order_service.update_order_subtotals(order_id)

    return redirect(url_for("order.get_order", order_id=order_id))


# ================================
#            DELETE
# ================================


@order_bp.post("/remove-item-from-order")
@permission_required(OrderPermissions.DELETE_TICKET_ITEM)
def remove_item_from_order():
    order_id = request.args.get("order_id")
    # order_item_id = request.args.get("order_item_id", type=int, default=0)
    # order_item_service.remove_item_from_order(order_item_id)
    order_service.update_order_subtotals(order_id)
    response = jsonify(success=True)
    response.headers["HX-Redirect"] = url_for("order.get_order", order_id=order_id)
    return response
