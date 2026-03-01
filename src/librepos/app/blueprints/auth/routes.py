"""Route handlers for auth blueprint."""
from flask import render_template

from . import bp


@bp.route("/")
def index():
    """List view for auth."""
    return render_template("auth/index.html")


@bp.route("/<int:id>")
def detail(id: int):
    """Detail view for a single auth item."""
    return render_template("auth/detail.html", id=id)
