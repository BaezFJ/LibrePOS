"""
File: routes.py
Author: [javier]
Date: [2/4/25]
Description:
    This module defines a set of routes and functionalities related to user management.
    It provides endpoints for creating, listing, viewing, editing, and deleting users,
    as well as ensuring appropriate permissions and authentication for each action.
"""

from flask import Blueprint, url_for, redirect, flash
from flask_login import current_user, login_required

from librepos.models import UserProfile
from librepos.models.user import User
from librepos.utils.decorators import permission_required
from librepos.utils.helpers import sanitize_form_data, generate_password
from .controller import UserController
from .forms import UserProfileForm, NewUserForm

user_bp = Blueprint("user", __name__, template_folder="templates")

user_controller = UserController


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    return user_controller().handle_login()


@user_bp.get("/logout")
@login_required
def logout():
    return user_controller().handle_logout()


@user_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Displays the logged-in user’s profile information and settings."""
    return user_controller().profile()


@user_bp.get("/users")
@login_required
@permission_required("ListUsers")
def list_users():
    """(Admin only) Lists all users in the system"""
    return user_controller().list_users()


@user_bp.get("/users/<string:user_id>/edit")
@login_required
@permission_required("UpdateUser")
def edit_user(user_id):
    """(Admin only) Allows an administrator to modify details or roles for a specific user."""
    return user_controller().edit_user(user_id=user_id)


@user_bp.get("/dashboard")
@login_required
def dashboard():
    """Displays the dashboard page for the logged-in user."""
    return user_controller().dashboard()


@user_bp.post("/new")
@permission_required("CreateUser")
def create_user():
    form = NewUserForm()
    if form.validate_on_submit():
        temp_password = generate_password()
        sanitized_data = sanitize_form_data(form)
        User.create(password=temp_password, **sanitized_data)
        flash("User created successfully.", "success")
    return redirect(url_for("user.list_users"))


@user_bp.post("/<string:user_id>/edit")
@permission_required("UpdateUser")
def update_user(user_id):
    # TODO 2/5/25 : implement update logic
    flash("This feature is not yet implemented.", "warning")
    return redirect(url_for("user.list_users"))


@user_bp.post("/<string:user_id>/delete")
@permission_required("DeleteUser")
def delete_user(user_id):
    # TODO 2/6/25 : implement delete login
    _user = User.query.filter_by(id=user_id).first_or_404()
    if _user:
        # TODO 2/8/25 : chang user status to deleted if history of sales if found, delete otherwise.
        _user.status = "DELETED"
        _user.update_instance()
        # _user.delete_instance()
        flash("User deleted successfully.", "success")
        return redirect(url_for("user.list_users"))
    flash("No user found", "danger")
    return redirect(url_for("user.list_users"))


@user_bp.post("/update-profile")
def update_profile():
    form = UserProfileForm()
    if form.validate_on_submit():
        _user_profile = UserProfile.query.filter_by(user_id=current_user.id).first()
        sanitized_data = sanitize_form_data(form)
        if _user_profile:
            UserProfile.update(_user_profile.id, **sanitized_data)
            flash("Profile updated successfully.", "success")
        else:
            UserProfile.create(user_id=current_user.id, **sanitized_data)
            flash("Profile created successfully.", "success")
        return redirect(url_for("user.list_users"))
    flash("Profile update failed.", "danger")
    return redirect(url_for("user.get_user_profile", user_id=current_user.id))
