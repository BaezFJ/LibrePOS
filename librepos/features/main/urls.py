from flask import Blueprint

from . import views

main_bp = Blueprint("main", __name__, template_folder="templates")

main_bp.add_url_rule("/", "get_dashboard", view_func=views.dashboard, methods=["GET"])
