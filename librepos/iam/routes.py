from flask import Blueprint, redirect, url_for

from . import views

iam_bp = Blueprint("iam", __name__, template_folder="templates", url_prefix="/iam")

iam_bp.add_url_rule("/", endpoint="index", view_func=lambda: redirect(url_for("iam.dashboard")))
iam_bp.add_url_rule("/dashboard", endpoint="dashboard", view_func=views.dashboard_view)
iam_bp.add_url_rule("/users", endpoint="users", view_func=views.users_view)
iam_bp.add_url_rule("/roles", endpoint="roles", view_func=views.roles_view)
iam_bp.add_url_rule("/policies", endpoint="policies", view_func=views.policies_view)
iam_bp.add_url_rule("/permissions", endpoint="permissions", view_func=views.permissions_view)
iam_bp.add_url_rule("/settings", endpoint="settings", view_func=views.settings_view)

iam_bp.add_url_rule("/login", endpoint="login", view_func=views.login_view, methods=["GET", "POST"])
iam_bp.add_url_rule("/logout", endpoint="logout", view_func=views.logout_view)
