"""
File: routes.py
Author: [javier]
Date: [2/1/25]
Description:
    This module is responsible for handling user authentication, including login, registration,
    and related functionality. It defines routes for the login and registration pages and
    integrates form validation and user authentication logic.
"""

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required

from librepos.blueprints.user.models.user import User, UserStatus
from librepos.utils.messages import Messages, display_message
from .forms import LoginForm

auth_bp = Blueprint("auth", __name__, template_folder="templates")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        display_message(Messages.AUTH_LOGGED_IN)
        return redirect(url_for("user.get_dashboard"))

    form = LoginForm()
    login_redirect = url_for("auth.login")
    context = {"title": "Login", "form": form}

    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username, status=UserStatus.ACTIVE).first()
        locked_user = User.query.filter_by(username=username, status=UserStatus.LOCKED).first()

        if locked_user:
            display_message(Messages.AUTH_LOCKED)
            return redirect(login_redirect)

        if user and not user.check_password(form.password.data):
            display_message(Messages.AUTH_FAILED)
            user.activity.update_failed_login_attempts()
            return redirect(login_redirect)

        if user and user.check_password(form.password.data):
            if not user.is_active:
                display_message(Messages.AUTH_LOCKED)
                return redirect(login_redirect)

            login_user(user, remember=form.remember_me.data)
            ip_address = request.remote_addr
            device_info = request.user_agent.string
            user.activity.update_activity(ip_address=ip_address, device_info=device_info)

            if user.activity.login_count == 1:
                target_profile_url = url_for("user.get_user_profile", user_id=user.id)
                display_message(Messages.AUTH_LOGIN)
                return redirect(target_profile_url)

            display_message(Messages.AUTH_LOGIN)
            return redirect(url_for("user.get_dashboard"))

        display_message(Messages.AUTH_FAILED)
        return redirect(login_redirect)
    return render_template("auth/login.html", **context)


@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    display_message(Messages.AUTH_LOGOUT)
    return redirect(url_for("auth.login"))
