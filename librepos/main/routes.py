from flask import Blueprint, render_template
from flask_login import login_required

main_bp = Blueprint("main", __name__, template_folder="templates")


@main_bp.before_request
@login_required
def before_request():
    """Force the user to log in before accessing any page."""
    pass


@main_bp.route("/")
def settings():
    context = {"title": "Settings"}
    return render_template("main/settings.html", **context)
