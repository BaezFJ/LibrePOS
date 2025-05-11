from flask import Blueprint, render_template, url_for, flash
from flask_login import current_user, login_required, fresh_login_required

from librepos.utils.decorators import permission_required
from librepos.utils import sanitize_form_data
from librepos.blueprints.auth.forms import PasswordResetForm

from .repositories import UserRepository
from .services import UserService
from .forms import UserProfileForm

user_bp = Blueprint("user", __name__, template_folder="templates", url_prefix="/users")

user_service = UserService(UserRepository())


@user_bp.before_request
@login_required
def authenticate_user_request():
    """Used to ensure that the user is authenticated before accessing any user-related views."""
    pass


@user_bp.route("/", methods=["GET", "POST"])
@permission_required("list_users")
def list_users():
    context = {
        "title": "Users",
        "users": user_service.get_all_users(),
    }
    return render_template("user/list_users.html", **context)


@user_bp.get("/settings")
def settings():
    return render_template("user/settings.html", title="Settings")


@user_bp.route("/settings/profile", methods=["GET", "POST"])
def profile():
    form = UserProfileForm()

    if current_user.profile:
        form = UserProfileForm(obj=current_user.profile)

    context = {
        "title": "Profile",
        "form": form,
        "back_url": url_for("user.settings"),
    }
    if form.validate_on_submit():
        sanitized_form_data = sanitize_form_data(form)
        user_service.update_profile(current_user.id, **sanitized_form_data)
        flash("Profile updated successfully.", "success")
    return render_template("user/profile.html", **context)


@user_bp.get("/settings/appearance")
def appearance():
    context = {
        "title": "Appearance",
        "back_url": url_for("user.settings"),
    }
    return render_template("user/appearance.html", **context)


@user_bp.get("/settings/notifications")
def notifications():
    context = {
        "title": "Notifications",
        "back_url": url_for("user.settings"),
    }
    return render_template("user/notifications.html", **context)


@user_bp.get("/settings/security")
def security():
    context = {
        "title": "Security",
        "back_url": url_for("user.settings"),
    }
    return render_template("user/security.html", **context)


@user_bp.route("/settings/security/password", methods=["GET", "POST"])
@fresh_login_required
def password():
    form = PasswordResetForm()
    context = {
        "title": "Password",
        "back_url": url_for("user.security"),
        "form": form,
    }
    return render_template("user/password.html", **context)


@user_bp.route("/settings/security/2fa", methods=["GET", "POST"])
def two_factor_auth():
    context = {
        "title": "2FA",
        "back_url": url_for("user.security"),
    }
    return render_template("user/two_factor_auth.html", **context)


@user_bp.route("/settings/security/questions")
def questions():
    context = {
        "title": "Questions",
        "back_url": url_for("user.security"),
    }
    return render_template("user/questions.html", **context)


@user_bp.get("/settings/security/sessions")
def sessions():
    context = {
        "title": "Sessions",
        "back_url": url_for("user.security"),
    }
    return render_template("user/sessions.html", **context)


@user_bp.get("/settings/accessibility")
def accessibility():
    context = {
        "title": "Accessibility",
        "back_url": url_for("user.settings"),
    }
    return render_template("user/accessibility.html", **context)
