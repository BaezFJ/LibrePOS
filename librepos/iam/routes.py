from flask import Blueprint

from . import views

iam_bp = Blueprint("iam", __name__, template_folder="templates", url_prefix="/iam")

iam_bp.add_url_rule("/login", endpoint="login", view_func=views.login_view, methods=["GET", "POST"])
iam_bp.add_url_rule("/logout", endpoint="logout", view_func=views.logout_view)
