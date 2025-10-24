from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

from librepos.utils import FlashMessageHandler
from .forms import AuthUserLoginForm
from .services import AuthenticationService

auth_bp = Blueprint("auth", __name__, template_folder="templates")

auth_user_service = AuthenticationService()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        FlashMessageHandler.warning("You are already logged in.")
        return redirect(url_for("core.home"))

    form = AuthUserLoginForm()
    context = {
        "title": "Login",
        "form": form,
    }

    if form.validate_on_submit():
        if auth_user_service.authenticate(
            form.username.data, form.password.data, form.remember.data
        ):
            return auth_user_service.handle_next_url()

    return render_template("auth/login.html", **context)


@auth_bp.route("/logout")
@login_required
def logout():
    auth_user_service.logout()
    return redirect(url_for("core.home"))
