from flask import Blueprint, render_template
from flask_login import login_required

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")


@dashboard_bp.before_request
@login_required
def before_request():
    pass


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
def get_dashboard():
    return render_template("dashboard.html")
