from flask import Blueprint, redirect, url_for

from . import views
from librepos.auth.views import login_view
from librepos.error.routes import error_bp
from librepos.auth.routes import iam_bp
from librepos.staff.routes import staff_bp

main_bp = Blueprint("main", __name__, template_folder="templates")

main_bp.add_url_rule("/", endpoint="index", view_func=lambda: redirect(url_for("main.dashboard")))
main_bp.add_url_rule("/dashboard", endpoint="dashboard", view_func=views.dashboard_view)

# Import login view from the auth module
main_bp.add_url_rule("/login", endpoint="login", view_func=login_view, methods=["GET", "POST"])


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(error_bp, url_prefix="/error")
    app.register_blueprint(iam_bp, url_prefix="/auth")
    app.register_blueprint(staff_bp, url_prefix="/staff")
