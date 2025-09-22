from flask import Blueprint, render_template, url_for, redirect, jsonify

from librepos.common.forms import ConfirmationForm
from librepos.utils.decorators import permission_required
from librepos.utils.form import sanitize_form_data
from ..forms import RoleCreationForm
from ..services import RoleService
from ..utils.enums import IAMPermissions as Permissions

role_service = RoleService()

role_bp = Blueprint("role", __name__, template_folder="templates", url_prefix="/roles")


# ================================
#            CREATE
# ================================


@role_bp.route("/new", methods=["POST", "GET"])
@permission_required(Permissions.CREATE_ROLE)
def create_role():
    """Display & process the creation role page."""
    form = RoleCreationForm()
    context = {
        "title": "Create Role",
        "back_url": url_for(".list_roles"),
        "form": form,
    }
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        new_role = role_service.create_role(sanitized_data)
        if new_role:
            return redirect(url_for(".get_role", role_id=new_role.id))
        return redirect(url_for(".list_roles"))
    return render_template("iam/role/create_role.html", **context)


# ================================
#            READ
# ================================


@role_bp.get("/")
@permission_required(Permissions.LIST_ROLE)
def list_roles():
    """Render the IAM roles page."""
    context = {
        "head_title": "IAM | Role | List",
        "head_description": "Define roles, assign access levels, and configure permissions across the system.",
        "roles": role_service.role_repository.get_all(),
    }
    return render_template("iam/role/list_roles.html", **context)


@role_bp.get("/<int:role_id>")
@permission_required(Permissions.READ_ROLE)
def get_role(role_id):
    """Render the IAM role page."""
    role = role_service.role_repository.get_by_id(role_id)
    form = ConfirmationForm()
    context = {
        "title": "Role",
        "back_url": url_for(".list_roles"),
        "role": role,
        "form": form,
        "update_role_permission": Permissions.UPDATE_ROLE,
    }
    return render_template("iam/role/get_role.html", **context)


@role_bp.get("/<int:role_id>/policies")
@permission_required(Permissions.UPDATE_ROLE)
def get_role_policies(role_id):
    role = role_service.role_repository.get_by_id(role_id)
    # unassigned_policies = role_service.get_unassigned_policies(role_id)
    context = {
        "title": role.name.title() if role else "Role",
        "back_url": url_for(".get_role", role_id=role_id),
        "role": role,
        "unassigned_policies": None,
    }
    return render_template("iam/role/role_policies.html", **context)


# ================================
#            UPDATE
# ================================


@role_bp.post("/<int:role_id>/toggle-suspend")
@permission_required(Permissions.UPDATE_ROLE)
def toggle_role_suspend(role_id):
    response = jsonify(success=True)
    role_service.toggle_role_status(role_id)
    response.headers["HX-Redirect"] = url_for(".get_role", role_id=role_id)
    return response


@role_bp.get("/<int:role_id>/assign-policy/<int:policy_id>")
@permission_required(Permissions.UPDATE_ROLE)
def assign_policy_to_role(role_id, policy_id):
    # role_service.assign_policy_to_role(role_id, policy_id)
    return redirect(url_for(".get_role_policies", role_id=role_id))


@role_bp.get("/<int:role_id>/unassign-policy/<int:policy_id>")
@permission_required(Permissions.UPDATE_ROLE)
def detach_policy_from_role(role_id, policy_id):
    # role_service.remove_policy_from_role(role_id, policy_id)
    return redirect(url_for(".get_role_policies", role_id=role_id))


# ================================
#            DELETE
# ================================
@role_bp.post("/<int:role_id>/delete")
@permission_required(Permissions.DELETE_ROLE)
def delete_role(role_id):
    form = ConfirmationForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        if role_service.delete_role(sanitized_data, role_id):
            return redirect(url_for(".list_roles"))
        return redirect(url_for(".get_role", role_id=role_id))
    return redirect(url_for(".get_role", role_id=role_id))
