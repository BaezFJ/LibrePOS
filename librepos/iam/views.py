from flask import current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from librepos.utils.images import delete_user_image, process_user_image
from librepos.utils.navigation import get_redirect_url

from .decorators import permission_required
from .forms import UserEditForm, UserLoginForm, UserRegisterForm
from .models import IAMUser, UserStatus
from .permissions import IAMPermissions
from .utils import authenticate_user


def dashboard_view():
    """Render the IAM dashboard page."""
    context = {
        "title": "Dashboard",
    }
    return render_template("iam/dashboard.html", **context)


@permission_required(IAMPermissions.VIEW_USERS)
def users_view():
    """Render the IAM Users page."""
    context = {
        "title": "Users",
        "users": IAMUser.get_all(),
    }
    return render_template("iam/users.html", **context)


@permission_required(IAMPermissions.CREATE_USERS)
def add_user_view():
    form = UserRegisterForm()
    context = {
        "title": "Add User",
        "form": form,
        "back_url": get_redirect_url("iam.users", param_name="back"),
    }
    if form.validate_on_submit():
        user = IAMUser(username=str(form.username.data), email=str(form.email.data))
        form.populate_obj(user)
        user.save()
        flash("User created successfully.", "success")
        return redirect(url_for("iam.users"))
    return render_template("iam/add_user.html", **context)


@permission_required(IAMPermissions.EDIT_USERS)
def edit_user_view(slug: str):
    """Render the edit user page."""
    user = IAMUser.get_first_by(slug=slug)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("iam.users"))

    form = UserEditForm(user=user, current_user=current_user, obj=user)
    if form.validate_on_submit():
        # Handle image upload before populate_obj
        new_image_path = None
        if form.image.data and hasattr(form.image.data, "filename") and form.image.data.filename:
            # Delete an old image if it exists and is not a default
            if user.image:
                delete_user_image(user.image, str(current_app.static_folder))

            # Process and save a new image
            new_image_path = process_user_image(
                file=form.image.data,
                username=user.username,
                static_folder=str(current_app.static_folder),
            )

        # Store the current image before populate_obj overwrites it
        current_image = user.image

        # Populate other fields
        form.populate_obj(user)

        # Restore/set the correct image path (not the FileStorage object)
        user.image = new_image_path if new_image_path else current_image

        user.save()
        flash("User updated successfully.", "success")
        return redirect(url_for("iam.users"))

    context = {
        "title": f"Edit User: {user.fullname}",
        "user": user,
        "form": form,
        "back_url": get_redirect_url("iam.users", param_name="back"),
    }
    return render_template("iam/edit_user.html", **context)


def roles_view():
    """Render the IAM Roles page."""
    context = {
        "title": "Roles",
    }
    return render_template("iam/roles.html", **context)


def policies_view():
    """Render the IAM Policies page."""
    context = {
        "title": "Policies",
    }
    return render_template("iam/policies.html", **context)


def permissions_view():
    """Render the IAM Permissions page."""
    context = {
        "title": "Permissions",
    }
    return render_template("iam/permissions.html", **context)


def settings_view():
    """Render the IAM Settings page."""
    context = {
        "title": "Settings",
    }
    return render_template("iam/settings.html", **context)


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
            if user.status == UserStatus.ACTIVE:
                login_user(user, remember=form.remember.data)
                flash(f"Welcome back {current_user.fullname}.", "success")
                return redirect(url_for("main.dashboard"))

            # Specific messages based on status
            if user.status == UserStatus.PENDING:
                flash("Your account is pending activation. Please check your email.", "warning")
            elif user.status in [UserStatus.SUSPENDED, UserStatus.DEACTIVATED]:
                flash(f"Your account is {user.status}. Please contact support.", "error")
            elif user.status == UserStatus.LOCKED:
                flash("Your account is locked. Please contact support.", "error")
            else:
                flash(
                    "There is an issue with your account. Please contact support for assistance.",
                    "error",
                )

            return redirect(url_for("iam.login"))

        flash("Invalid credentials. Please try again.", "error")
        return redirect(url_for("iam.login"))

    return render_template("iam/login.html", **context)


def logout_view():
    """Log the user out."""
    logout_user()
    return redirect(url_for("iam.login"))
