from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required
from librepos.features.auth.decorators import permission_required

from .forms import CreateUserForm, CreateGroupForm
from .permissions import IAMPermissions
from .services import IAMService
from ...utils import sanitize_form_data

iam_service = IAMService()

iam_bp = Blueprint("iam", __name__, template_folder="templates")


@iam_bp.get("/")
@iam_bp.route("/home")
@login_required
def home():
    context = {
        "title": "IAM | Home",
        "back_url": url_for("core.home"),
    }
    return render_template("iam/home.html", **context)


# ================================
#            USERS
# ================================
@iam_bp.route("/users/list", endpoint="list_users", methods=["GET"])
@permission_required(IAMPermissions.VIEW_IAM_USER)
def list_users():
    context = {
        "title": "IAM | List | Users",
        "back_url": url_for("iam.home"),
        "users": iam_service.iam_user_repo.get_all(),
    }
    return render_template("iam/list_users.html", **context)


@iam_bp.route("/users/create", endpoint="create_user", methods=["GET", "POST"])
@permission_required(IAMPermissions.CREATE_IAM_USER)
def create_user():
    form = CreateUserForm()
    context = {
        "title": "IAM | Create | User",
        "back_url": url_for("iam.list_users"),
        "form": form,
    }
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        iam_service.create_user(sanitized_data)
        return redirect(url_for("iam.list_users"))
    return render_template("iam/create_user.html", **context)


@iam_bp.get("/users/<int:user_id>")
@permission_required(IAMPermissions.VIEW_IAM_USER)
def view_user(user_id):
    user = iam_service.iam_user_repo.get_by_id(user_id)
    context = {
        "title": "IAM | View | User",
        "back_url": url_for("iam.list_users"),
        "user": user,
    }
    return render_template("iam/view_user.html", **context)


# ================================
#          PERMISSIONS
# ================================
@iam_bp.get("/permissions/list")
@permission_required(IAMPermissions.VIEW_IAM_PERMISSION)
def list_permissions():
    context = {
        "title": "IAM | List | Permissions",
        "back_url": url_for("iam.home"),
        "permissions": iam_service.iam_permission_repo.get_all(),
    }
    return render_template("iam/list_permissions.html", **context)


# ================================
#            GROUPS
# ================================
@iam_bp.get("/groups/list")
@permission_required(IAMPermissions.VIEW_IAM_GROUP)
def list_groups():
    context = {
        "title": "IAM | List | Groups",
        "back_url": url_for("iam.home"),
        "groups": iam_service.iam_user_group_repo.get_all(),
    }
    return render_template("iam/list_groups.html", **context)


@iam_bp.get("/groups/<int:group_id>")
@permission_required(IAMPermissions.VIEW_IAM_GROUP)
def view_group(group_id):
    group = iam_service.iam_user_group_repo.get_by_id(group_id)
    context = {
        "title": "IAM | View | Group",
        "back_url": url_for("iam.list_groups"),
        "group": group,
    }
    return render_template("iam/view_group.html", **context)


@iam_bp.route("/groups/<int:group_id>/edit", methods=["GET", "POST"])
@permission_required(IAMPermissions.DELETE_IAM_GROUP)
def edit_group(group_id):
    group = iam_service.iam_user_group_repo.get_by_id(group_id)
    form = CreateGroupForm(obj=group)
    context = {
        "title": "IAM | Edit | Group",
        "back_url": url_for("iam.view_group", group_id=group_id),
        "form": form,
        "group": group,
    }
    if form.validate_on_submit():
        pass
    return render_template("iam/edit_group.html", **context)


@iam_bp.get("/groups/<int:group_id>/users")
@permission_required(IAMPermissions.VIEW_IAM_GROUP)
def view_group_users(group_id):
    group = iam_service.iam_user_group_repo.get_by_id(group_id)
    context = {
        "title": "IAM | View | Group Users",
        "back_url": url_for("iam.view_group", group_id=group_id),
        "group": group,
    }
    return render_template("iam/view_group_users.html", **context)


@iam_bp.route("/groups/create", methods=["GET", "POST"])
@permission_required(IAMPermissions.CREATE_IAM_GROUP)
def create_group():
    form = CreateGroupForm()
    context = {
        "title": "IAM | Create | Group",
        "back_url": url_for("iam.list_groups"),
        "form": form,
    }
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        iam_service.create_group(sanitized_data)
        return redirect(url_for("iam.list_groups"))

    return render_template("iam/create_group.html", **context)
