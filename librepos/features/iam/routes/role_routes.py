from flask import Blueprint, render_template, url_for, redirect, jsonify

from librepos.common.forms import ConfirmationForm
from librepos.utils.decorators import permission_required
from librepos.utils.form import sanitize_form_data
from ..forms import RoleCreationForm
from ..services import RoleService

role_service = RoleService()

role_bp = Blueprint("role", __name__, template_folder="templates", url_prefix="/roles")


# ================================
#            CREATE
# ================================


@role_bp.post("/create")
@permission_required("iam.create.role")
def process_create_role():
    """Process the role creation form."""
    form = RoleCreationForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        role = role_service.create_role(sanitized_data)
        if role:
            return redirect(url_for(".get_role", role_id=role.id))
    return redirect(url_for(".list_roles"))


# ================================
#            READ
# ================================


@role_bp.get("/")
@permission_required("iam.list.roles")
def list_roles():
    """Render the IAM roles page."""
    context = {
        "title": "Roles",
        "description": "Define roles, assign access levels, and configure permissions across the system.",
        "back_url": url_for("iam.home"),
        "roles": role_service.role_repository.get_all(),
        "form": RoleCreationForm(),
    }
    return render_template("iam/role/list_roles.html", **context)


@role_bp.get("/create")
@permission_required("iam.create.role")
def display_create_role():
    """Render the IAM role creation page."""
    form = RoleCreationForm()
    context = {
        "title": "Create Role",
        "back_url": url_for(".list_roles"),
        "form": form,
    }
    return render_template("iam/role/create_role.html", **context)


@role_bp.get("/<int:role_id>")
@permission_required("iam.read.role")
def get_role(role_id):
    """Render the IAM role page."""
    role = role_service.role_repository.get_by_id(role_id)
    form = ConfirmationForm()
    context = {
        "title": "Role",
        "back_url": url_for(".list_roles"),
        "role": role,
        "form": form,
    }
    return render_template("iam/role/get_role.html", **context)


@role_bp.get("/<int:role_id>/policies")
@permission_required("iam.assign.policy_to_role")
def get_role_policies(role_id):
    role = role_service.role_repository.get_by_id(role_id)
    unassigned_policies = role_service.get_unassigned_policies(role_id)
    context = {
        "title": role.name.title() if role else "Role",
        "back_url": url_for(".get_role", role_id=role_id),
        "role": role,
        "unassigned_policies": unassigned_policies,
    }
    return render_template("iam/role/role_policies.html", **context)


# ================================
#            UPDATE
# ================================


@role_bp.post("/<int:role_id>/toggle-suspend")
@permission_required("iam.suspend.role")
def toggle_role_suspend(role_id):
    response = jsonify(success=True)
    role_service.toggle_role_status(role_id)
    response.headers["HX-Redirect"] = url_for(".get_role", role_id=role_id)
    return response


@role_bp.get("/<int:role_id>/assign-policy/<int:policy_id>")
@permission_required("iam.assign.policy_to_role")
def assign_policy_to_role(role_id, policy_id):
    role_service.assign_policy_to_role(role_id, policy_id)
    return redirect(url_for(".get_role_policies", role_id=role_id))


@role_bp.get("/<int:role_id>/unassign-policy/<int:policy_id>")
@permission_required("iam.assign.policy_to_role")
def detach_policy_from_role(role_id, policy_id):
    role_service.remove_policy_from_role(role_id, policy_id)
    return redirect(url_for(".get_role_policies", role_id=role_id))


# ================================
#            DELETE
# ================================
@role_bp.post("/<int:role_id>/delete")
@permission_required("iam.delete.role")
def delete_role(role_id):
    form = ConfirmationForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        if role_service.delete_role(sanitized_data, role_id):
            return redirect(url_for(".list_roles"))
        return redirect(url_for(".get_role", role_id=role_id))
    return redirect(url_for(".get_role", role_id=role_id))
