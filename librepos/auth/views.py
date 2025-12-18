from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from librepos.utils.navigation import get_redirect_url

from .forms import UserLoginForm, UserRegisterForm
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


def register_view():
    form = UserRegisterForm()
    back_url = get_redirect_url("main.dashboard", param_name="back")
    context = {
        "title": "Register",
        "form": form,
        "back_url": back_url,
    }
    if form.validate_on_submit():
        AuthUser.create(
            email=form.email.data,
            username=form.username.data,
            unsecure_password=form.password.data,
            first_name=form.first_name.data,
            middle_name=form.middle_name.data,
            last_name=form.last_name.data,
            role_id=form.role_id.data,
        )
        flash("Registration successful. Please login.")
        return redirect(back_url or url_for("auth.login"))
    return render_template("auth/register.html", **context)
