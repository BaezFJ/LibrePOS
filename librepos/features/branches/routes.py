from flask import Blueprint, render_template, url_for, redirect

from librepos.utils import sanitize_form_data
from librepos.utils.decorators import permission_required
from .forms import BranchForm
from .services import BranchService

branch_bp = Blueprint(
    "branch", __name__, template_folder="templates", url_prefix="/branches"
)

branch_service = BranchService()


# ======================================================================================================================
#                                              BRANCH ROUTES
# ======================================================================================================================


# ================================
#            READ
# ================================


@branch_bp.get("/")
@permission_required("branch.list")
def list_branches():
    context = {
        "title": "Branches",
        "back_url": url_for("settings.home"),
        "branches": branch_service.repository.get_all(),
    }
    return render_template("branches/list_branches.html", **context)


@branch_bp.get("/<int:branch_id>>")
@permission_required("branch.read")
def get_branch(branch_id):
    """Render the branch page."""
    branch = branch_service.repository.get_by_id(branch_id)
    form = BranchForm(obj=branch)
    context = {
        "title": "Branches",
        "back_url": url_for(".list_branches"),
        "branch": branch,
        "form": form,
    }
    return render_template("branches/get_branch.html", **context)


# ================================
#            UPDATE
# ================================
@branch_bp.post("/<int:branch_id>/update-branch>")
@permission_required("branch.update")
def update_restaurant(branch_id):
    form = BranchForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        branch_service.update_restaurant(sanitized_data)
    return redirect(url_for(".get_branch", branch_id=branch_id))
