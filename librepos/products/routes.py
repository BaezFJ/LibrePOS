from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from librepos.utils import sanitize_form_data
from librepos.auth.decorators import permission_required

from .forms import ProductForm
from .service import ProductService

product_bp = Blueprint(
    "product", __name__, template_folder="templates", url_prefix="/products"
)

product_service = ProductService()


@product_bp.before_request
@login_required
def before_request():
    """Force the user to log in before accessing any page."""
    pass


@product_bp.route("/", methods=["GET", "POST"])
@permission_required("list_products")
def list_products():
    products = product_service.list_products()
    form = ProductForm()
    context = {"title": "Products", "products": products, "form": form}
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        product_service.create_product(sanitized_data)
        return redirect(url_for(".list_products"))
    return render_template("products/list_products.html", **context)


@product_bp.route("/<int:product_id>", methods=["GET", "POST"])
@permission_required("get_product")
def get_product(product_id):
    product = product_service.get_product(product_id)
    form = ProductForm(obj=product)
    context = {
        "title": product.name if product else "Details",
        "back_url": url_for(".list_products"),
        "product": product,
        "form": form,
    }
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        product_service.update_product(product_id, sanitized_data)
        return redirect(url_for(".get_product", product_id=product_id))
    return render_template("products/get_product.html", **context)
