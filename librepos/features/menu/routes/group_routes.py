from flask import Blueprint, render_template, redirect, url_for

from librepos.common.forms import ConfirmationForm
from librepos.utils import sanitize_form_data
from librepos.utils.decorators import permission_required
from ..forms import MenuGroupForm
from ..services import MenuGroupService

group_bp = Blueprint(
    "group", __name__, template_folder="templates", url_prefix="/groups"
)

menu_group_service = MenuGroupService()


# ================================
#            CREATE
# ================================
@group_bp.route("/create", methods=["POST", "GET"])
@permission_required("menu.create.group")
def create_group():
    """Display & process the creation group page."""
    form = MenuGroupForm()
    context = {
        "title": "Group",
        "back_url": url_for(".list_groups"),
        "form": form,
    }
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        new_group = menu_group_service.create_group(sanitized_data)
        if new_group:
            return redirect(url_for(".get_group", group_id=new_group.id))
    return render_template("menu/group/create_group.html", **context)


# ================================
#            READ
# ================================
@group_bp.get("/")
@permission_required("menu.list.groups")
def list_groups():
    form = MenuGroupForm()
    context = {
        "title": "Groups",
        "back_url": url_for("menu.home"),
        "groups": menu_group_service.repository.get_all(),
        "form": form,
    }
    return render_template("menu/group/list_groups.html", **context)


@group_bp.get("/<int:group_id>")
@permission_required("menu.read.group")
def get_group(group_id):
    context = {
        "title": "Group",
        "back_url": url_for("menu.group.list_groups"),
        "group": menu_group_service.repository.get_by_id(group_id),
        "form": ConfirmationForm(),
    }
    return render_template("menu/group/get_group.html", **context)


# ================================
#            UPDATE
# ================================
@group_bp.route("/<int:group_id>/update", methods=["POST", "GET"])
@permission_required("menu.update.group")
def update_group(group_id):
    group = menu_group_service.repository.get_by_id(group_id)
    form = MenuGroupForm(obj=group, submit_text="Update")
    context = {
        "title": "Update",
        "back_url": url_for(".get_group", group_id=group_id),
        "form": form,
        "group": group,
    }
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        menu_group_service.update_group(group_id, sanitized_data)
        return redirect(url_for(".get_group", group_id=group_id))
    return render_template("menu/group/update_group.html", **context)


# ================================
#            DELETE
# ================================
@group_bp.post("/<int:group_id>/delete")
@permission_required("menu.delete.group")
def delete_group(group_id):
    form = ConfirmationForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        if menu_group_service.delete_group(group_id, sanitized_data):
            return redirect(url_for(".list_groups"))
        return redirect(url_for(".get_group", group_id=group_id))
    return redirect(url_for(".list_groups"))
