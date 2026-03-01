"""Route handlers for auth blueprint."""
from flask import render_template

from . import bp


@bp.route("/")
def index():
    """List view for auth."""
    context = {
        "head_title": "Auth | LibrePOS",
        "appbar_title": "Auth"
    }
    return render_template("auth/index.html", **context)


@bp.route("/<int:id>")
def detail(id: int):
    """Detail view for a single auth item."""
    return render_template("auth/detail.html", id=id)
