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
from .forms import UserForm
from ...utils.helpers import sanitize_form_data

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
    _user = User.get_by_id(current_user.id)
    context = {
        "title": "Dashboard",
        "user": _user,
    }
    return render_template("user/dashboard.html", **context)


@user_bp.post("/new")
@permission_required("create_user")
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        User.create(**sanitized_data)
        flash("User created successfully.", "success")
    return redirect(url_for("user.list_users"))


@user_bp.get("/list")
@permission_required("ListUsers")
def list_users():
    _users = User.get_all()
    form = UserForm()
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
    context = {
        "title": f"{_user.username if _user else 'not found'}",
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
    flash("This feature is not yet implemented.", "warning")
    return redirect(url_for("user.list_users"))
