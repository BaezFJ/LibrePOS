from flask import Blueprint, url_for, render_template

from librepos.utils.decorators import permission_required
from ..services import PolicyService
from ..utils.enums import IAMPermissions

policy_service = PolicyService()

policy_bp = Blueprint(
    "policy", __name__, template_folder="templates", url_prefix="/policies"
)


# ================================
#            READ
# ================================
@policy_bp.get("/policies")
@permission_required(IAMPermissions.LIST_POLICY)
def list_policies():
    """Render the IAM policies page."""
    context = {
        "title": "Policies",
        "description": "A policy controls what users can and cannot do in LibrePOS, like which buttons they can click and which screens they can view.",
        "back_url": url_for("iam.home"),
        "policies": policy_service.policy_repository.get_all(),
    }
    return render_template("iam/policy/list_policies.html", **context)


@policy_bp.get("/policies/<int:policy_id>")
@permission_required(IAMPermissions.READ_POLICY)
def get_policy(policy_id):
    """Render the IAM policy page."""
    policy = policy_service.policy_repository.get_by_id(policy_id)
    policy_permissions = policy_service.get_policy_permissions(policy_id)
    context = {
        "title": "Policy",
        "back_url": url_for(".list_policies"),
        "policy": policy,
        "policy_permissions": policy_permissions,
    }
    return render_template("iam/policy/get_policy.html", **context)
