from flask import Blueprint, render_template, url_for, jsonify
from flask_login import login_required

from librepos.auth.decorators import permission_required
from librepos.menu.service import MenuService

from .service import OrderService

order_bp = Blueprint(
    "order", __name__, template_folder="templates", url_prefix="/orders"
)

order_service = OrderService()
menu_service = MenuService()


@order_bp.before_request
@login_required
def before_request():
    """Force the user to log in before accessing any page."""
    pass


# ================================
#            CREATE
# ================================
@order_bp.post("/create-order")
@permission_required("create_order")
def create_order():
    new_order = order_service.create_order()
    response = jsonify(success=True)
    response.headers["HX-Redirect"] = url_for("order.get_order", order_id=new_order.id)
    return response


# ================================
#            READ
# ================================
@order_bp.get("/")
@permission_required("list_orders")
def list_orders():
    context = {
        "title": "Orders",
        "orders": order_service.list_user_pending_orders(),
    }
    return render_template("order/list_orders.html", **context)


@order_bp.get("/<int:order_id>")
@permission_required("get_order")
def get_order(order_id):
    order = order_service.get_order(order_id)
    menu_categories = menu_service.list_menu_categories()
    context = {
        "title": str(order.order_number),
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
@permission_required("void_order")
def void_order(order_id):
    order_service.mark_order_as_voided(order_id)
    response = jsonify(success=True)
    response.headers["HX-Redirect"] = url_for("order.list_orders")
    return response


@order_bp.post("/add-item-to-order/<int:order_id>/<int:item_id>")
def add_item_to_order(order_id, item_id):
    order_service.add_item_to_order(order_id, item_id)
    response = jsonify(success=True)
    response.headers["HX-Redirect"] = url_for("order.get_order", order_id=order_id)
    return response


# ================================
#            DELETE
# ================================
