from flask import Blueprint, redirect, url_for

from . import views

main_bp = Blueprint("main", __name__, template_folder="templates")

main_bp.add_url_rule("/", endpoint="index", view_func=lambda: redirect(url_for("main.dashboard")))
main_bp.add_url_rule("/dashboard", endpoint="dashboard", view_func=views.dashboard_view)
