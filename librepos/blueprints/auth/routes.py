"""
File: routes.py
Author: [javier]
Date: [2/1/25]
Description:
    This module is responsible for handling user authentication, including login, registration,
    and related functionality. It defines routes for the login and registration pages and
    integrates form validation and user authentication logic.
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from librepos.blueprints.user.models.user import User
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
        # user = authenticate_user(form.email.data, form.password.data)
        _user = User.query.filter_by(email=form.email.data).first()
        if _user and not _user.is_active:
            flash(
                "Your account is not active. Please contact the site administrator.",
                "danger",
            )
            return redirect(url_for("auth.login"))
        if _user:
            login_user(_user, remember=form.remember_me.data)
            flash(f"Welcome back, {_user.email}! You are now logged in.", "success")
            return redirect(url_for("user.get_dashboard"))
        else:
            flash("Invalid credentials.", "danger")
    return render_template("auth/login.html", **context)


@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
