from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from librepos.utils.navigation import get_redirect_url

from .forms import UserLoginForm
from .models import AuthUser


def login_view():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = UserLoginForm()
    context = {
        "title": "Login",
        "form": form,
    }
    if form.validate_on_submit():
        user = AuthUser.get_first_by(email=str(form.email.data))

        if user is None or not user.check_password(str(form.password.data)):
            flash("Invalid email or password.")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember.data)
        flash(f"Welcome back {user.fullname}.")
        return redirect(get_redirect_url("main.dashboard"))
    return render_template("auth/login.html", **context)


def logout_view():
    logout_user()
    return redirect(url_for("auth.login"))
