from flask import Blueprint, redirect, url_for

from . import views

iam_bp = Blueprint("iam", __name__, template_folder="templates", url_prefix="/iam")

iam_bp.add_url_rule("/", endpoint="index", view_func=lambda: redirect(url_for("iam.dashboard")))
iam_bp.add_url_rule("/dashboard", endpoint="dashboard", view_func=views.dashboard_view)
iam_bp.add_url_rule(
    "/dashboard/activity",
    endpoint="dashboard_activity",
    view_func=views.dashboard_activity_view,
)

# =============================================================================
# User Management Routes
# =============================================================================
iam_bp.add_url_rule("/users", endpoint="users", view_func=views.users_view)
iam_bp.add_url_rule("/users/<slug>", endpoint="user", view_func=views.user_view, methods=["GET"])
iam_bp.add_url_rule(
    "/users/add", endpoint="add_user", view_func=views.add_user_view, methods=["GET", "POST"]
)
iam_bp.add_url_rule(
    "/users/<slug>/profile",
    endpoint="user_profile",
    view_func=views.user_profile_view,
    methods=["GET", "POST"],
)
iam_bp.add_url_rule(
    "/users/<slug>/account",
    endpoint="user_account",
    view_func=views.user_account_view,
    methods=["GET", "POST"],
)
iam_bp.add_url_rule(
    "/users/<slug>/address",
    endpoint="user_address",
    view_func=views.user_address_view,
    methods=["GET", "POST"],
)
iam_bp.add_url_rule(
    "/users/<slug>/update-image",
    endpoint="update_user_image",
    view_func=views.update_user_image_view,
    methods=["POST"],
)
iam_bp.add_url_rule(
    "/users/<slug>/reset-password",
    endpoint="reset_user_password",
    view_func=views.reset_user_password_view,
    methods=["GET", "POST"],
)
iam_bp.add_url_rule(
    "/users/<slug>/lock",
    endpoint="lock_user",
    view_func=views.lock_user_view,
    methods=["POST"],
)
iam_bp.add_url_rule(
    "/users/<slug>/unlock",
    endpoint="unlock_user",
    view_func=views.unlock_user_view,
    methods=["POST"],
)
iam_bp.add_url_rule(
    "/users/<slug>/delete",
    endpoint="delete_user",
    view_func=views.delete_user_view,
    methods=["POST"],
)
iam_bp.add_url_rule(
    "/users/<slug>/login-history",
    endpoint="user_login_history",
    view_func=views.user_login_history_view,
    methods=["GET"],
)
iam_bp.add_url_rule(
    "/users/<slug>/settings",
    endpoint="user_settings",
    view_func=views.user_settings_view,
    methods=["GET"],
)
iam_bp.add_url_rule(
    "/users/<slug>/resend-invitation",
    endpoint="resend_invitation",
    view_func=views.resend_invitation_view,
    methods=["POST"],
)

# =============================================================================
# Invitation Routes (Public - No Auth Required)
# =============================================================================
iam_bp.add_url_rule(
    "/invitation/<token>",
    endpoint="accept_invitation",
    view_func=views.accept_invitation_view,
    methods=["GET", "POST"],
)

# =============================================================================
# Role Management Routes
# =============================================================================
iam_bp.add_url_rule("/roles", endpoint="roles", view_func=views.roles_view)

# =============================================================================
# Policies Management Routes
# =============================================================================
iam_bp.add_url_rule("/policies", endpoint="policies", view_func=views.policies_view)

# =============================================================================
# Permissions Management Routes
# =============================================================================
iam_bp.add_url_rule("/permissions", endpoint="permissions", view_func=views.permissions_view)

# =============================================================================
# Settings Management Routes
# =============================================================================
iam_bp.add_url_rule("/settings", endpoint="settings", view_func=views.settings_view)

# =============================================================================
# Authentication Management Routes
# =============================================================================
iam_bp.add_url_rule("/login", endpoint="login", view_func=views.login_view, methods=["GET", "POST"])
iam_bp.add_url_rule("/logout", endpoint="logout", view_func=views.logout_view)
iam_bp.add_url_rule(
    "/forgot-password",
    endpoint="forgot_password",
    view_func=views.forgot_password_view,
    methods=["GET", "POST"],
)
iam_bp.add_url_rule(
    "/reset-password/<token>",
    endpoint="reset_password",
    view_func=views.reset_password_view,
    methods=["GET", "POST"],
)
iam_bp.add_url_rule(
    "/confirm-password",
    endpoint="confirm_password",
    view_func=views.confirm_password_view,
    methods=["GET", "POST"],
)
