from flask import Blueprint, render_template, request, redirect, url_for, flash
from .service import AuthService
from flask_login import login_required

from .forms import LoginForm

auth_bp = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")

auth_service = AuthService()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if auth_service.current_user().is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("main.settings"))

    form = LoginForm()
    context = {
        "title": "Login",
        "form": form,
    }
    if form.validate_on_submit():
        user = auth_service.authenticate(form.email.data, form.password.data)
        if user:
            user.record_sign_in(
                ip=str(request.remote_addr), agent=str(request.user_agent)[:255]
            )
            return redirect(request.args.get("next") or url_for("main.settings"))
    return render_template("auth/login.html", **context)


@auth_bp.get("/logout")
@login_required
def logout():
    auth_service.logout()
    flash("Logged out successfully.", "success")
    return redirect(url_for(".login"))
