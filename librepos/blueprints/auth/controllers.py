from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from .services import AuthService
from .forms import LoginForm, ReauthenticateForm

auth_bp = Blueprint("auth", __name__, template_folder="templates")

auth_service = AuthService()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Render the login page."""

    if auth_service.authenticated_user():
        flash("You are already logged in.", "info")
        return redirect(url_for("user.list_users"))

    form = LoginForm()

    context = {
        "title": "Login",
        "form": form,
    }

    if form.validate_on_submit():
        username = str(form.username.data)
        password = str(form.password.data)
        user = auth_service.authenticate(username, password)
        if user:
            flash(f"Welcome back! {user.username}")
            return redirect(request.args.get("next") or url_for("user.list_users"))
        flash("Invalid username or password.", "danger")

    return render_template("auth/login.html", **context)


@auth_bp.route("/logout")
@login_required
def logout():
    auth_service.logout()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/reauthenticate")
@login_required
def reauthenticate():
    """Force the user to reauthenticate."""
    form = ReauthenticateForm()
    context = {
        "title": "Reauthenticate",
        "form": form,
    }
    return render_template("auth/reauthenticate.html", **context)
