"""
File: routes.py
Author: [javier]
Date: [2/4/25]
Description:
    This module defines a set of routes and functionalities related to user management.
    It provides endpoints for creating, listing, viewing, editing, and deleting users,
    as well as ensuring appropriate permissions and authentication for each action.
"""

from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required, current_user

from librepos.blueprints.user.models.user import User
from librepos.utils.decorators import permission_required
from .forms import UserForm, UserProfileForm, NewUserForm
from .models import UserProfile
from ...utils.helpers import sanitize_form_data, generate_password

user_bp = Blueprint("user", __name__, template_folder="templates", url_prefix="/user")


@user_bp.before_request
@login_required
def before_request():
    """
    Decorator to require a user to be logged in before processing a request. This
    function is registered to be invoked before each request handled by the
    decorated blueprint. It leverages the Flask-Login's `@login_required`
    decorator to enforce user authentication.

    :return: None
    """
    pass


@user_bp.get("/dashboard")
def get_dashboard():
    context = {
        "title": "Dashboard",
    }
    return render_template("user/dashboard.html", **context)


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


@user_bp.get("/list")
@permission_required("ListUsers")
def list_users():
    _users = User.get_all()
    form = NewUserForm()
    context = {
        "title": "Users",
        "users": _users,
        "form": form,
        "back_url": url_for("user.get_dashboard"),
    }
    return render_template("user/list_users.html", **context)


@user_bp.get("/<string:user_id>")
@permission_required("GetUser")
def get_user(user_id):
    _user = User.get_by_id(user_id)
    form = UserForm(obj=_user)
    title = _user.username if _user else "User"
    context = {
        "title": title,
        "user": _user,
        "form": form,
        "back_url": url_for("user.list_users"),
    }
    return render_template("user/view_user.html", **context)


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


@user_bp.get("/<string:user_id>/profile")
def get_user_profile(user_id):
    _user_profile = UserProfile.query.filter_by(user_id=user_id).first()
    form = UserProfileForm(obj=_user_profile)
    context = {
        "title": "Profile",
        "form": form,
        "back_url": url_for("user.get_dashboard"),
    }
    return render_template("user/user_profile.html", **context)


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
