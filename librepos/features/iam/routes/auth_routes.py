from urllib.parse import urlparse

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from librepos.utils import FlashMessageHandler
from ..forms import UserLoginForm
from ..services import AuthService

auth_bp = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")

auth_service = AuthService()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        FlashMessageHandler.warning("You are already logged in.")
        return redirect(url_for("dashboard"))

    form = UserLoginForm()
    context = {
        "form": form,
    }
    if form.validate_on_submit():
        ip = str(request.remote_addr)
        agent = str(request.user_agent)[:255]
        if auth_service.authenticate(
                form.username.data, form.password.data, form.remember.data, ip, agent
        ):
            next_url = request.args.get("next", "")
            next_url = next_url.replace("\\", "")  # Normalize backslashes
            if not urlparse(next_url).netloc and not urlparse(next_url).scheme:
                return redirect(next_url or url_for("dashboard"))
            return redirect(url_for("dashboard"))
    return render_template("iam/auth/login.html", **context)


@auth_bp.get("/logout")
@login_required
def logout():
    auth_service.logout()
    return redirect(url_for(".login"))
