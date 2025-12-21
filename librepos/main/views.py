from flask import render_template
from flask_login import login_required


def access_denied(e):
    return render_template("main/error/403.html"), 403


def page_not_found(e):
    return render_template("main/error/404.html"), 404


def internal_server_error(e):
    return render_template("main/error/500.html"), 500


@login_required
def dashboard_view():
    context = {
        "title": "Dashboard",
    }
    return render_template("main/dashboard.html", **context)
