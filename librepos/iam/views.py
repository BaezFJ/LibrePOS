from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from librepos.iam.forms import UserLoginForm
from librepos.iam.utils import authenticate_user


def login_view():
    """Render the login page."""

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = UserLoginForm()
    context = {
        "title": "Login",
        "form": form,
    }
    if form.validate_on_submit():
        identity = str(form.credentials.data)
        password = str(form.password.data)
        user = authenticate_user(identity, password)
        if user:
            login_user(user, remember=form.remember.data)
            flash(f"Welcome back {current_user.fullname}.", "success")
            return redirect(url_for("main.dashboard"))
        flash("Invalid credentials. Please try again.", "error")
        return redirect(url_for("iam.login"))

    return render_template("iam/login.html", **context)


def logout_view():
    """Log the user out."""
    logout_user()
    return redirect(url_for("iam.login"))
