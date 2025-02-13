from flask import Blueprint
from flask_login import login_required

from .controller import DashboardController

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")

dashboard_controller = DashboardController


@dashboard_bp.before_request
@login_required
def before_request():
    """
    Ensures that the user is authenticated before accessing any route 
    associated with the dashboard blueprint.
    """
    pass


@dashboard_bp.get("/dashboard")
def get_dashboard():
    return dashboard_controller().show_dashboard()


@dashboard_bp.get("/overview")
def get_overview():
    return dashboard_controller().show_overview()
