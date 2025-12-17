from flask import Blueprint

from . import views

iam_bp = Blueprint("auth", __name__, template_folder="templates")

iam_bp.add_url_rule("/login", endpoint="login", view_func=views.login_view, methods=["GET", "POST"])
iam_bp.add_url_rule("/logout", endpoint="logout", view_func=views.logout_view)
