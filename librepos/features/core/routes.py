from flask import Blueprint, render_template, url_for
from flask_login import login_required

core_bp = Blueprint("core", __name__, template_folder="templates")


@core_bp.route("/")
@login_required
def dashboard():
    return render_template("core/dashboard.html")


@core_bp.route("/help")
def get_help():
    context = {
        "title": "Help",
        "back_url": url_for("core.dashboard"),
    }
    return render_template("core/help.html", **context)
