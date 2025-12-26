from flask import Blueprint, redirect, url_for

from . import views

iam_bp = Blueprint("iam", __name__, template_folder="templates", url_prefix="/iam")

iam_bp.add_url_rule("/", endpoint="index", view_func=lambda: redirect(url_for("iam.dashboard")))
iam_bp.add_url_rule("/dashboard", endpoint="dashboard", view_func=views.dashboard_view)
iam_bp.add_url_rule("/users", endpoint="users", view_func=views.users_view)
iam_bp.add_url_rule(
    "/users/add", endpoint="add_user", view_func=views.add_user_view, methods=["GET", "POST"]
)
iam_bp.add_url_rule(
    "/users/<slug>/edit",
    endpoint="edit_user",
    view_func=views.edit_user_view,
    methods=["GET", "POST"],
)
iam_bp.add_url_rule(
    "/users/<slug>/image",
    endpoint="update_user_image",
    view_func=views.update_user_image_view,
    methods=["POST"],
)
iam_bp.add_url_rule(
    "/users/<slug>/profile",
    endpoint="update_user_profile",
    view_func=views.update_user_profile_view,
    methods=["POST"],
)
iam_bp.add_url_rule("/roles", endpoint="roles", view_func=views.roles_view)
iam_bp.add_url_rule("/policies", endpoint="policies", view_func=views.policies_view)
iam_bp.add_url_rule("/permissions", endpoint="permissions", view_func=views.permissions_view)
iam_bp.add_url_rule("/settings", endpoint="settings", view_func=views.settings_view)

iam_bp.add_url_rule("/login", endpoint="login", view_func=views.login_view, methods=["GET", "POST"])
iam_bp.add_url_rule("/logout", endpoint="logout", view_func=views.logout_view)
