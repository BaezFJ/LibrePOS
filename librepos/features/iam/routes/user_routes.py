from flask import Blueprint, render_template, url_for, redirect, jsonify

from librepos.common.forms import ConfirmationForm
from librepos.utils.decorators import permission_required
from librepos.utils.form import sanitize_form_data
from ..forms import (
    UserCreationForm,
    UserContactForm,
    UserAddressForm,
    UserDetailsForm,
    UserRoleForm,
)
from ..services import UserService

user_service = UserService()

user_bp = Blueprint("user", __name__, template_folder="templates", url_prefix="/users")


# ================================
#            CREATE
# ================================
@user_bp.post("/create-user")
@permission_required("iam.create.user")
def process_create_user():
    """Process the user creation form."""
    form = UserCreationForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        user = user_service.create_user(sanitized_data)
        if user:
            return redirect(url_for(".display_update_user", user_id=user.id))
    return redirect(url_for(".display_create_user"))


# ================================
#            READ
# ================================
@user_bp.get("/")
@permission_required("iam.list.user")
def list_users():
    users = user_service.user_repository.get_all()
    form = UserCreationForm()
    context = {
        "title": "Users",
        "description": "An IAM Users are accounts that can log in and use the LibrePOS system based on their permissions.",
        "back_url": url_for("iam.home"),
        "users": users,
        "form": form,
    }
    return render_template("iam/user/list_users.html", **context)


@user_bp.get("/<int:user_id>")
@permission_required("iam.read.user")
def get_user(user_id):
    """Render the user page."""
    user = user_service.user_repository.get_by_id(user_id)
    form = ConfirmationForm()
    context = {
        "title": "User",
        "back_url": url_for(".list_users"),
        "user": user,
        "form": form,
    }
    return render_template("iam/user/get_user.html", **context)


@user_bp.get("/create")
@permission_required("iam.create.user")
def display_create_user():
    """Render the IAM user creation page."""
    form = UserCreationForm()
    context = {
        "title": "Create User",
        "back_url": url_for(".list_users"),
        "form": form,
    }
    return render_template("iam/user/create_user.html", **context)


@user_bp.get("/<int:user_id>/update")
@permission_required("iam.update.user")
def display_update_user(user_id):
    """Render the IAM user update page."""
    user = user_service.user_repository.get_by_id(user_id)
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
    return render_template("iam/user/update_user.html", **context)


@user_bp.get("/<int:user_id>/role-change")
@permission_required("iam.update.user")
def display_role_change(user_id):
    """Render the IAM user role change page."""
    user = user_service.user_repository.get_by_id(user_id)
    form = UserRoleForm(obj=user)
    context = {
        "title": "Change Role",
        "back_url": url_for(".get_user", user_id=user_id),
        "form": form,
        "user": user,
    }
    return render_template("iam/user/role_change.html", **context)


# ================================
#            UPDATE
# ================================
@user_bp.post("/<int:user_id>/update/address")
@permission_required("iam.update.user")
def update_user_address(user_id):
    form = UserAddressForm()
    if form.validate_on_submit:
        sanitized_data = sanitize_form_data(form)
        user_service.update_user(user_id, sanitized_data)
    return redirect(url_for(".display_update_user", user_id=user_id))


@user_bp.post("/<int:user_id>/update/contact")
@permission_required("iam.update.user")
def update_user_contact(user_id):
    form = UserContactForm()
    if form.validate_on_submit:
        sanitized_data = sanitize_form_data(form)
        user_service.update_user(user_id, sanitized_data)
    return redirect(url_for(".display_update_user", user_id=user_id))


@user_bp.post("/<int:user_id>/update/details")
@permission_required("iam.update.user")
def update_user_details(user_id):
    form = UserDetailsForm()
    if form.validate_on_submit:
        sanitized_data = sanitize_form_data(form)
        user_service.update_user(user_id, sanitized_data)
    return redirect(url_for(".display_update_user", user_id=user_id))


@user_bp.post("/<int:user_id>/suspend")
@permission_required("iam.suspend.user")
def toggle_user_suspend(user_id):
    response = jsonify(success=True)
    user_service.toggle_user_status(user_id)
    response.headers["HX-Redirect"] = url_for(".get_user", user_id=user_id)
    return response


@user_bp.post("/<int:user_id>/update-role")
@permission_required("iam.update.user")
def update_user_role(user_id):
    form = UserRoleForm()
    if form.validate_on_submit:
        sanitized_data = sanitize_form_data(form)
        user_service.update_user(user_id, sanitized_data)
    return redirect(url_for(".get_user", user_id=user_id))


# ================================
#            DELETE
# ================================
@user_bp.post("/<int:user_id>/delete")
@permission_required("iam.delete.user")
def delete_user(user_id):
    """Render the IAM user creation page."""
    form = ConfirmationForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        user_service.delete_user(sanitized_data)
    return redirect(url_for(".list_users"))
