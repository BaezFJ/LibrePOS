from flask import Blueprint, render_template, url_for, redirect, jsonify
from flask_login import login_required

from librepos.forms import (
    RoleForm,
    UserCreationForm,
    ConfirmDeletionForm,
    UserContactForm,
    UserAddressForm,
    UserDetailsForm,
    UserRoleForm,
)
from librepos.services.iam_service import IAMService
from librepos.utils.decorators import permission_required
from librepos.utils.form import sanitize_form_data

iam_service = IAMService()

iam_bp = Blueprint("iam", __name__, template_folder="templates", url_prefix="/iam")


@iam_bp.before_request
@login_required
def before_request():
    """Force the user to log in before accessing any page."""
    pass


@iam_bp.get("/")
@iam_bp.get("/home")
@permission_required("iam.access")
def home():
    """Render the IAM home page."""

    context = {
        "title": "IAM",
        "back_url": url_for("settings.home"),
    }
    return render_template("iam/home.html", **context)


# ======================================================================================================================
#                                              USERS ROUTES
# ======================================================================================================================


# ================================
#            CREATE
# ================================
@iam_bp.post("/users/create")
@permission_required("iam.create.user")
def process_create_user():
    """Process the user creation form."""
    form = UserCreationForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        user = iam_service.create_user(sanitized_data)
        if user:
            return redirect(url_for(".display_update_user", user_id=user.id))
    return redirect(url_for(".display_create_user"))


# ================================
#            READ
# ================================
@iam_bp.get("/users")
@permission_required("iam.list.user")
def list_users():
    users = iam_service.user_repository.get_all()
    form = UserCreationForm()
    context = {
        "title": "Users",
        "back_url": url_for(".home"),
        "users": users,
        "form": form,
    }
    return render_template("iam/list_users.html", **context)


@iam_bp.get("/users/<int:user_id>")
@permission_required("iam.read.user")
def get_user(user_id):
    """Render the user page."""
    user = iam_service.user_repository.get_by_id(user_id)
    form = ConfirmDeletionForm(id=user_id)
    context = {
        "title": "User",
        "back_url": url_for(".list_users"),
        "user": user,
        "form": form,
    }
    return render_template("iam/get_user.html", **context)


@iam_bp.get("/users/create")
@permission_required("iam.create.user")
def display_create_user():
    """Render the IAM user creation page."""
    form = UserCreationForm()
    context = {
        "title": "Create User",
        "back_url": url_for(".list_users"),
        "form": form,
    }
    return render_template("iam/create_user.html", **context)


@iam_bp.get("/users/<int:user_id>/update")
@permission_required("iam.update.user")
def display_update_user(user_id):
    """Render the IAM user update page."""
    user = iam_service.user_repository.get_by_id(user_id)
    contact_form = UserContactForm(obj=user)
    address_form = UserAddressForm(obj=user)
    details_form = UserDetailsForm(obj=user)
    context = {
        "title": "Update User",
        "back_url": url_for(".get_user", user_id=user_id),
        "user": user,
        "contact_form": contact_form,
        "address_form": address_form,
        "details_form": details_form,
    }
    return render_template("iam/update_user.html", **context)


@iam_bp.get("/users/<int:user_id>/role-change")
@permission_required("iam.update.user")
def display_role_change(user_id):
    """Render the IAM user role change page."""
    user = iam_service.user_repository.get_by_id(user_id)
    form = UserRoleForm(obj=user)
    context = {
        "title": "Change Role",
        "back_url": url_for(".get_user", user_id=user_id),
        "form": form,
        "user": user,
    }
    return render_template("iam/role_change.html", **context)


# ================================
#            UPDATE
# ================================
@iam_bp.post("/users/update/address/<int:user_id>")
@permission_required("iam.update.user")
def update_user_address(user_id):
    form = UserAddressForm()
    if form.validate_on_submit:
        sanitized_data = sanitize_form_data(form)
        iam_service.update_user(user_id, sanitized_data)
    return redirect(url_for(".display_update_user", user_id=user_id))


@iam_bp.post("/users/update/contact/<int:user_id>")
@permission_required("iam.update.user")
def update_user_contact(user_id):
    form = UserContactForm()
    if form.validate_on_submit:
        sanitized_data = sanitize_form_data(form)
        iam_service.update_user(user_id, sanitized_data)
    return redirect(url_for(".display_update_user", user_id=user_id))


@iam_bp.post("/users/update/details/<int:user_id>")
@permission_required("iam.update.user")
def update_user_details(user_id):
    form = UserDetailsForm()
    if form.validate_on_submit:
        sanitized_data = sanitize_form_data(form)
        iam_service.update_user(user_id, sanitized_data)
    return redirect(url_for(".display_update_user", user_id=user_id))


@iam_bp.post("/users/<int:user_id>/suspend")
@permission_required("iam.suspend.user")
def toggle_user_suspend(user_id):
    response = jsonify(success=True)
    iam_service.toggle_user_status(user_id)
    response.headers["HX-Redirect"] = url_for(".get_user", user_id=user_id)
    return response


@iam_bp.post("/users/<int:user_id>/update-role")
@permission_required("iam.update.user")
def update_user_role(user_id):
    form = UserRoleForm()
    if form.validate_on_submit:
        sanitized_data = sanitize_form_data(form)
        iam_service.update_user(user_id, sanitized_data)
    return redirect(url_for(".get_user", user_id=user_id))


# ================================
#            DELETE
# ================================
@iam_bp.post("/users/delete/<int:user_id>")
@permission_required("iam.delete.user")
def delete_user(user_id):
    """Render the IAM user creation page."""
    form = ConfirmDeletionForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        iam_service.delete_user(sanitized_data)
    return redirect(url_for(".list_users"))


# ======================================================================================================================
#                                              ROLES ROUTES
# ======================================================================================================================

# ================================
#            CREATE
# ================================


@iam_bp.post("/roles/create")
@permission_required("iam.create.role")
def process_create_role():
    """Process the role creation form."""
    form = RoleForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        role = iam_service.create_role(sanitized_data)
        if role:
            return redirect(url_for(".get_role", role_id=role.id))
    return redirect(url_for(".list_roles"))


# ================================
#            READ
# ================================


@iam_bp.get("/roles")
@permission_required("iam.list.roles")
def list_roles():
    """Render the IAM roles page."""
    context = {
        "title": "Roles",
        "back_url": url_for(".home"),
        "roles": iam_service.role_repository.get_all(),
        "form": RoleForm(),
    }
    return render_template("iam/list_roles.html", **context)


@iam_bp.get("/roles/create")
@permission_required("iam.create.role")
def display_create_role():
    """Render the IAM role creation page."""
    form = RoleForm()
    context = {
        "title": "Create Role",
        "back_url": url_for(".list_roles"),
        "form": form,
    }
    return render_template("iam/create_rol.html", **context)


@iam_bp.get("/roles/<int:role_id>")
@permission_required("iam.read.role")
def get_role(role_id):
    """Render the IAM role page."""
    role = iam_service.role_repository.get_by_id(role_id)
    form = ConfirmDeletionForm(id=role_id)
    context = {
        "title": "Role",
        "back_url": url_for(".list_roles"),
        "role": role,
        "form": form,
    }
    return render_template("iam/get_role.html", **context)


@iam_bp.get("/roles/<int:role_id>/policies")
@permission_required("iam.assign.policy_to_role")
def get_role_policies(role_id):
    role = iam_service.role_repository.get_by_id(role_id)
    context = {
        "title": role.name.title() if role else "Role",
        "back_url": url_for(".get_role", role_id=role_id),
        "role": role,
    }
    return render_template("iam/role_policies.html", **context)


# ================================
#            UPDATE
# ================================


@iam_bp.post("/roles/<int:role_id>/toggle-suspend")
@permission_required("iam.suspend.role")
def toggle_role_suspend(role_id):
    response = jsonify(success=True)
    iam_service.toggle_role_status(role_id)
    response.headers["HX-Redirect"] = url_for(".get_role", role_id=role_id)
    return response


# ================================
#            DELETE
# ================================
@iam_bp.post("/roles/delete/<int:role_id>")
@permission_required("iam.delete.role")
def delete_role(role_id):
    form = ConfirmDeletionForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        iam_service.delete_role(sanitized_data, role_id)
        return redirect(url_for(".list_roles"))
    return redirect(url_for(".get_role", role_id=role_id))
