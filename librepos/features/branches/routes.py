from flask import Blueprint, render_template, url_for, redirect

from librepos.utils import sanitize_form_data
from librepos.utils.decorators import permission_required
from .forms import BranchForm
from .services import BranchService

branch_bp = Blueprint('branch', __name__, template_folder='templates', url_prefix='/branches')

branch_service = BranchService()


# ======================================================================================================================
#                                              RESTAURANT ROUTES
# ======================================================================================================================


# ================================
#            READ
# ================================
@branch_bp.get("/")
@permission_required("restaurant.read")
def get_restaurant():
    restaurant = branch_service.repository.get_by_id(1)
    form = BranchForm(obj=restaurant)
    context = {
        "title": "Branches",
        "back_url": url_for(".home"),
        "restaurant": restaurant,
        "form": form,
    }
    return render_template("branches/get_restaurant.html", **context)


# ================================
#            UPDATE
# ================================
@branch_bp.post("/<branch_id>/update-branch>")
@permission_required("restaurant.update")
def update_restaurant():
    form = BranchForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        branch_service.update_restaurant(sanitized_data)
    return redirect(url_for(".get_restaurant"))
