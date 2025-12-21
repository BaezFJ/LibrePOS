from flask import Blueprint, redirect, url_for

from . import views

staff_bp = Blueprint("staff", __name__, template_folder="templates", url_prefix="/staff")

staff_bp.add_url_rule("/", endpoint="index", view_func=lambda: redirect(url_for("staff.members")))
staff_bp.add_url_rule("/members", endpoint="members", view_func=views.members_view)
staff_bp.add_url_rule("/roles", endpoint="roles", view_func=views.roles_view)

# staff_bp.add_url_rule("/<int:staff_id>", endpoint="detail", view_func=views.detail_view)
# staff_bp.add_url_rule("/add", endpoint="add", view_func=views.add_view)
# staff_bp.add_url_rule("/edit/<int:staff_id>", endpoint="edit", view_func=views.edit_view)
