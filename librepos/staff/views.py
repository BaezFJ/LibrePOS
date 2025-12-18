from flask import render_template

from librepos.auth.decorators import permission_required
from librepos.auth.config import Permissions
from librepos.auth import models as auth_models


@permission_required(Permissions.VIEW_EMPLOYEES)
def members_view():
    context = {
        "title": "Members",
        "users": auth_models.AuthUser.get_all(),
    }
    return render_template("staff/members.html", **context)


def roles_view():
    context = {
        "title": "Roles",
        "roles": auth_models.AuthRole.get_all(),
    }
    return render_template("staff/roles.html", **context)
