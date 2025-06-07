from urllib.parse import urlparse

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from librepos.utils import FlashMessageHandler
from librepos.forms import UserLoginForm
from librepos.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, template_folder="templates")

auth_service = AuthService()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        FlashMessageHandler.warning("You are already logged in.")
        return redirect(url_for("order.list_orders"))

    form = UserLoginForm()
    context = {
        "title": "Login",
        "form": form,
    }
    if form.validate_on_submit():
        user = auth_service.authenticate(
            form.email.data, form.password.data, form.remember.data
        )
        if user:
            user.record_sign_in(
                ip=str(request.remote_addr), agent=str(request.user_agent)[:255]
            )
            next_url = request.args.get("next", "")
            next_url = next_url.replace("\\", "")  # Normalize backslashes
            if not urlparse(next_url).netloc and not urlparse(next_url).scheme:
                return redirect(next_url or url_for("order.list_orders"))
            return redirect(url_for("order.list_orders"))
    return render_template("auth/login.html", **context)


@auth_bp.get("/logout")
@login_required
def logout():
    auth_service.logout()
    return redirect(url_for(".login"))
