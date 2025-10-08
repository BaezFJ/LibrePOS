from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from librepos.utils import FlashMessageHandler

from ..forms import UserLoginForm
from ..services import AuthenticationService

auth_bp = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")

auth_service = AuthenticationService()


@auth_bp.route("/login", methods=["GET", "POST"])
def get_login():

    if current_user.is_authenticated:
        FlashMessageHandler.info("You are already logged in.")
        return redirect(url_for("main.get_dashboard"))

    form = UserLoginForm()
    context = {
        "form": form,
    }
    if form.validate_on_submit():
        ip = str(request.remote_addr)
        agent = str(request.user_agent)[:255]
        if auth_service.authenticate(form.username.data, form.password.data, form.remember.data):
            auth_service.handle_tracking(ip, agent)
            return auth_service.handle_next_url()
    return render_template("iam/auth/login.html", **context)


@auth_bp.get("/logout")
@login_required
def logout():
    auth_service.logout()
    return redirect(url_for(".get_login"))
