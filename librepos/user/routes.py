from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_required, current_user

from librepos.utils import sanitize_form_data
from librepos.auth.decorators import permission_required

from .service import UserService
from .forms import NewUserForm, UserContactDetailsForm

users_bp = Blueprint("user", __name__, template_folder="templates", url_prefix="/users")

user_service = UserService()


@users_bp.before_request
@login_required
def before_request():
    """Force the user to log in before accessing any page."""
    pass


@users_bp.route("/", methods=["GET", "POST"])
@permission_required("list_users")
def list_users():
    users = user_service.list_users()
    form = NewUserForm()
    context = {
        "title": "Users",
        "back_url": url_for("main.settings"),
        "users": users,
        "form": form,
    }

    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        new_user = user_service.create_user(sanitized_data)
        flash(f"User {new_user.email} created successfully.", "success")
        return redirect(url_for("user.list_users"))

    return render_template("user/list_users.html", **context)


@users_bp.get("/<int:user_id>")
@permission_required("get_user")
def get_user(user_id):
    context = {
        "title": "User",
        "back_url": url_for("user.list_users"),
        "user": user_service.get_user(user_id),
    }
    return render_template("user/get_user.html", **context)


@users_bp.route("/profile", methods=["GET", "POST"])
def profile():
    """Render the user's profile page."""
    form = UserContactDetailsForm(obj=current_user)
    context = {
        "title": "Profile",
        "back_url": url_for("main.settings"),
        "form": form,
    }
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        user_service.update_user(current_user.id, sanitized_data)
        flash("Profile updated successfully.", "success")
        return redirect(url_for("user.profile"))
    return render_template("user/profile.html", **context)
