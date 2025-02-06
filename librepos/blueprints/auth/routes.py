"""
File: routes.py
Author: [javier]
Date: [2/1/25]
Description:
    This module is responsible for handling user authentication, including login, registration,
    and related functionality. It defines routes for the login and registration pages and
    integrates form validation and user authentication logic.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from librepos.blueprints.user.models.user import User, UserStatus
from .forms import LoginForm

auth_bp = Blueprint("auth", __name__, template_folder="templates")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("user.get_dashboard"))
    form = LoginForm()
    context = {
        "title": "Login",
        "form": form,
    }
    if form.validate_on_submit():
        _user = User.query.filter_by(
            email=form.email.data, status=UserStatus.ACTIVE
        ).first()

        # check if the user account is locked
        _user_locked = User.query.filter_by(
            email=form.email.data, status=UserStatus.LOCKED
        ).first()
        if _user_locked:
            flash(
                "Your account is locked. Please contact the site administrator.",
                "danger",
            )
            return redirect(url_for("auth.login"))

        # Incorrect password used
        if _user and not _user.check_password(form.password.data):
            flash("Invalid credentials please try again.", "danger")
            _user.activity.update_failed_login_attempts()
            return redirect(url_for("auth.login"))

        if _user and _user.check_password(form.password.data):
            # user is not active
            if not _user.is_active:
                flash(
                    "Your account is not active. Please contact the site administrator.",
                    "danger",
                )
                return redirect(url_for("auth.login"))

            # login user
            login_user(_user, remember=form.remember_me.data)

            # update the user activity (login count, ip_address, device)
            _ip_address = request.remote_addr
            _device_info = request.user_agent.string
            _user.activity.update_activity(
                ip_address=_ip_address, device_info=_device_info
            )

            if _user.profile.first_name and _user.profile.last_name:
                flash(
                    f"Welcome, {_user.profile.full_name}! You are now logged in.",
                    "success",
                )
            else:
                flash(f"Welcome, {_user.email}! You are now logged in.", "success")

            return redirect(url_for("user.get_dashboard"))

        flash("Invalid credentials please try again.", "danger")
        return redirect(url_for("auth.login"))
    return render_template("auth/login.html", **context)


@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
