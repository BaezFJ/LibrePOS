from flask import render_template

from librepos.iam.decorators import permission_required
from librepos.iam.models import IAMRole, IAMUser

from .permissions import StaffPermissions


@permission_required(StaffPermissions.VIEW_EMPLOYEES)
def members_view():
    context = {
        "title": "Members",
        "users": IAMUser.get_all(),
    }
    return render_template("staff/members.html", **context)


def roles_view():
    context = {
        "title": "Roles",
        "roles": IAMRole.get_all(),
    }
    return render_template("staff/roles.html", **context)
