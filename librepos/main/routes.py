from flask import Blueprint, redirect, url_for

from . import views
from librepos.staff.routes import staff_bp
from librepos.iam.routes import iam_bp

main_bp = Blueprint("main", __name__, template_folder="templates", url_prefix="/")

main_bp.add_url_rule("/", endpoint="index", view_func=lambda: redirect(url_for("main.dashboard")))
main_bp.add_url_rule("/dashboard", endpoint="dashboard", view_func=views.dashboard_view)

# Error pages
main_bp.app_errorhandler(403)(views.access_denied)
main_bp.app_errorhandler(404)(views.page_not_found)
main_bp.app_errorhandler(500)(views.internal_server_error)

# Redirects
main_bp.add_url_rule(
    "/login", endpoint="login_redirect", view_func=lambda: redirect(url_for("iam.login"))
)
main_bp.add_url_rule(
    "/logout", endpoint="logout_redirect", view_func=lambda: redirect(url_for("iam.logout"))
)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(iam_bp)
    app.register_blueprint(staff_bp)
