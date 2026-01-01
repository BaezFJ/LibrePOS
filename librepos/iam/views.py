from flask import abort, current_app, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from librepos.extensions import db
from librepos.utils.export import ExportField, export_to_csv
from librepos.utils.images import delete_user_image, process_user_image
from librepos.utils.navigation import get_redirect_url, is_safe_url

from .decorators import REAUTH_SESSION_KEY, permission_required, reauthenticate_required
from .forms import (
    AdminResetPasswordForm,
    ConfirmActionForm,
    PasswordConfirmForm,
    UserAddressForm,
    UserEditForm,
    UserImageForm,
    UserLoginForm,
    UserProfileForm,
    UserRegisterForm,
)
from .models import IAMRole, IAMUser, IAMUserAddress, IAMUserProfile, UserStatus
from .permissions import IAMPermissions
from .utils import authenticate_user

# Export field definitions for users
USER_EXPORT_FIELDS = [
    ExportField("Username", lambda u: u.username),
    ExportField("Email", lambda u: u.email),
    ExportField("Role", lambda u: u.role.name if u.role else "N/A"),
    ExportField("Status", lambda u: u.status.value.title()),
    ExportField(
        "Last Login",
        lambda u: u.last_login_at.strftime("%Y-%m-%d %H:%M") if u.last_login_at else "Never",
    ),
]


def dashboard_view():
    """Render the IAM dashboard page."""
    context = {
        "title": "Dashboard",
    }
    return render_template("iam/dashboard.html", **context)


# =============================================================================
# User Management Views
# =============================================================================


@permission_required(IAMPermissions.VIEW_USERS)
def users_view():
    """Render the IAM Users page."""
    form = UserRegisterForm(current_user=current_user)

    # Handle search
    search_query = request.args.get("q", "").strip()

    # Handle filtering by status
    status_filter = request.args.get("status", "")
    valid_statuses = {s.value for s in UserStatus}

    # Handle sorting
    sort_field = request.args.get("sort", "username")
    sort_options = {
        "username": IAMUser.username,
        "role": IAMRole.name,
        "last_active": IAMUser.last_login_at.desc(),
        "status": IAMUser.status,
    }

    # Build query
    query = db.select(IAMUser)

    # Apply search filter
    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.where(
            db.or_(
                IAMUser.username.ilike(search_pattern),
                IAMUser.email.ilike(search_pattern),
            )
        )

    # Apply status filter if valid
    if status_filter in valid_statuses:
        query = query.where(IAMUser.status == status_filter)

    # Apply sorting
    if sort_field == "role":
        query = query.outerjoin(IAMRole).order_by(sort_options[sort_field])
    elif sort_field in sort_options:
        query = query.order_by(sort_options[sort_field])
    else:
        query = query.order_by(IAMUser.username)

    users = db.session.execute(query).scalars().all()

    # Handle export
    export_format = request.args.get("export", "")
    if export_format == "csv":
        return export_to_csv(users, USER_EXPORT_FIELDS, "users_export")

    context = {
        "title": "Users",
        "users": users,
        "form": form,
        "breadcrumb": [
            {"url": url_for("iam.dashboard"), "label": "IAM"},
            {"url": None, "label": "Users"},
        ],
    }
    return render_template("iam/users.html", **context)


@permission_required(IAMPermissions.VIEW_USERS)
def user_view(slug: str | None = None):
    user = IAMUser.query.filter_by(slug=slug).first()
    if not user:
        abort(404, description="User not found")

    display_name = user.profile.fullname if user.profile else user.username
    context = {
        "title": user.username.title(),
        "user": user,
        "back_url": get_redirect_url("iam.users", param_name="back"),
        "breadcrumb": [
            {"url": url_for("iam.dashboard"), "label": "IAM"},
            {"url": url_for("iam.users"), "label": "Users"},
            {"url": None, "label": display_name},
        ],
    }
    return render_template("iam/user.html", **context)


@permission_required(IAMPermissions.VIEW_USERS)
def user_profile_view(slug: str):
    """View and edit user profile information."""
    user = IAMUser.get_first_by(slug=slug)
    if not user:
        abort(404, description="User not found")

    form = UserProfileForm(obj=user.profile) if user.profile else UserProfileForm()
    image_form = UserImageForm()

    if form.validate_on_submit():
        # Check edit permission for POST
        if not current_user.has_permission(IAMPermissions.EDIT_USERS):
            abort(403)

        if not user.profile:
            user.profile = IAMUserProfile(
                first_name=str(form.first_name.data or ""),
                last_name=str(form.last_name.data or ""),
                user_id=user.id,
            )

        form.populate_obj(user.profile)
        user.profile.save()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("iam.user_profile", slug=slug))

    display_name = user.profile.fullname if user.profile else user.username
    context = {
        "title": f"{display_name} - Profile",
        "user": user,
        "form": form,
        "image_form": image_form,
        "back_url": url_for("iam.user", slug=slug),
        "breadcrumb": [
            {"url": url_for("iam.dashboard"), "label": "IAM"},
            {"url": url_for("iam.users"), "label": "Users"},
            {"url": url_for("iam.user", slug=slug), "label": display_name},
            {"url": None, "label": "Profile"},
        ],
    }
    return render_template("iam/user_profile.html", **context)


@permission_required(IAMPermissions.VIEW_USERS)
def user_account_view(slug: str):
    """View and edit user account details (username, email, role)."""
    user = IAMUser.get_first_by(slug=slug)
    if not user:
        abort(404, description="User not found")

    form = UserEditForm(user=user, current_user=current_user, obj=user)

    if form.validate_on_submit():
        # Check edit permission for POST
        if not current_user.has_permission(IAMPermissions.EDIT_USERS):
            abort(403)

        user.username = str(form.username.data)
        user.email = str(form.email.data)
        user.role_id = form.role_id.data
        user.save()
        flash("Account updated successfully.", "success")
        return redirect(url_for("iam.user_account", slug=user.slug))

    display_name = user.profile.fullname if user.profile else user.username
    context = {
        "title": f"{display_name} - Account",
        "user": user,
        "form": form,
        "back_url": url_for("iam.user", slug=slug),
        "breadcrumb": [
            {"url": url_for("iam.dashboard"), "label": "IAM"},
            {"url": url_for("iam.users"), "label": "Users"},
            {"url": url_for("iam.user", slug=slug), "label": display_name},
            {"url": None, "label": "Account"},
        ],
    }
    return render_template("iam/user_account.html", **context)


@permission_required(IAMPermissions.VIEW_USERS)
def user_address_view(slug: str):
    """View and edit user address information."""
    user = IAMUser.get_first_by(slug=slug)
    if not user:
        abort(404, description="User not found")

    form = UserAddressForm(obj=user.address) if user.address else UserAddressForm()

    if form.validate_on_submit():
        # Check edit permission for POST
        if not current_user.has_permission(IAMPermissions.EDIT_USERS):
            abort(403)

        if not user.address:
            user.address = IAMUserAddress(user_id=user.id)

        form.populate_obj(user.address)
        user.address.save()
        flash("Address updated successfully.", "success")
        return redirect(url_for("iam.user_address", slug=slug))

    display_name = user.profile.fullname if user.profile else user.username
    context = {
        "title": f"{display_name} - Address",
        "user": user,
        "form": form,
        "back_url": url_for("iam.user", slug=slug),
        "breadcrumb": [
            {"url": url_for("iam.dashboard"), "label": "IAM"},
            {"url": url_for("iam.users"), "label": "Users"},
            {"url": url_for("iam.user", slug=slug), "label": display_name},
            {"url": None, "label": "Address"},
        ],
    }
    return render_template("iam/user_address.html", **context)


@permission_required(IAMPermissions.CREATE_USERS)
def add_user_view():
    form = UserRegisterForm()
    if form.validate_on_submit():
        user = IAMUser(
            username=str(form.username.data),
            email=str(form.email.data),
            first_name=str(form.first_name.data),
            last_name=str(form.last_name.data),
            role_id=form.role_id.data,
        )
        user.save()
        flash("User created successfully.", "success")
        return redirect(url_for("iam.edit_user", slug=user.slug))
    flash("Form validation failed. Please check your input.", "error")
    return redirect(url_for("iam.users"))


@permission_required(IAMPermissions.EDIT_USERS)
def update_user_image_view(slug: str):
    """Handle user profile image upload."""
    user = IAMUser.get_first_by(slug=slug)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("iam.users"))

    form = UserImageForm()
    if form.validate_on_submit():
        # Delete old image if it exists and is not a default
        if user.profile.image:
            delete_user_image(user.profile.image, str(current_app.static_folder))

        # Process and save new image
        image_path = process_user_image(
            file=form.image.data,
            username=user.username,
            static_folder=str(current_app.static_folder),
        )
        user.profile.image = image_path
        user.profile.save()
        flash("Profile image updated successfully.", "success")
    else:
        for error in form.image.errors:
            flash(error, "error")

    return redirect(url_for("iam.user_profile", slug=slug))


@permission_required(IAMPermissions.EDIT_USERS)
@reauthenticate_required
def reset_user_password_view(slug: str):
    """Handle admin resetting a user's password."""
    user = IAMUser.get_first_by(slug=slug)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("iam.users"))

    form = AdminResetPasswordForm()
    display_name = user.profile.fullname if user.profile else user.username
    context = {
        "title": "Reset Password",
        "user": user,
        "form": form,
        "back_url": url_for("iam.user", slug=slug),
        "breadcrumb": [
            {"url": url_for("iam.dashboard"), "label": "IAM"},
            {"url": url_for("iam.users"), "label": "Users"},
            {"url": url_for("iam.user", slug=slug), "label": display_name},
            {"url": None, "label": "Reset Password"},
        ],
    }
    if form.validate_on_submit():
        user.set_password(str(form.new_password.data))
        user.save()
        flash(f"Password for {user.profile.fullname} has been reset successfully.", "success")
        return redirect(url_for("iam.user", slug=slug))

    return render_template("iam/reset_password.html", **context)


@permission_required(IAMPermissions.EDIT_USERS)
def lock_user_view(slug: str):
    """Lock a user account."""
    user = IAMUser.get_first_by(slug=slug)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("iam.users"))

    # Validate password confirmation
    form = ConfirmActionForm()
    if not form.validate_on_submit():
        flash("Password confirmation required.", "error")
        return redirect(url_for("iam.user", slug=slug))

    if not current_user.check_password(str(form.password.data)):
        flash("Incorrect password.", "error")
        return redirect(url_for("iam.user", slug=slug))

    # Prevent locking yourself
    if user.id == current_user.id:
        flash("You cannot lock your own account.", "error")
        return redirect(url_for("iam.user", slug=slug))

    # Prevent locking already locked users
    if user.status == UserStatus.LOCKED:
        flash("This account is already locked.", "warning")
        return redirect(url_for("iam.user", slug=slug))

    user.status = UserStatus.LOCKED
    user.save()
    flash(f"Account for {user.profile.fullname} has been locked.", "success")
    return redirect(url_for("iam.user", slug=slug))


@permission_required(IAMPermissions.EDIT_USERS)
def unlock_user_view(slug: str):
    """Unlock a user account."""
    user = IAMUser.get_first_by(slug=slug)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("iam.users"))

    # Validate password confirmation
    form = ConfirmActionForm()
    if not form.validate_on_submit():
        flash("Password confirmation required.", "error")
        return redirect(url_for("iam.user", slug=slug))

    if not current_user.check_password(str(form.password.data)):
        flash("Incorrect password.", "error")
        return redirect(url_for("iam.user", slug=slug))

    # Only locked accounts can be unlocked
    if user.status != UserStatus.LOCKED:
        flash("This account is not locked.", "warning")
        return redirect(url_for("iam.user", slug=slug))

    user.status = UserStatus.ACTIVE
    user.save()
    flash(f"Account for {user.profile.fullname} has been unlocked.", "success")
    return redirect(url_for("iam.user", slug=slug))


@permission_required(IAMPermissions.EDIT_USERS)
def delete_user_view(slug: str):
    """Soft delete a user account (sets status to DELETED)."""
    user = IAMUser.get_first_by(slug=slug)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("iam.users"))

    # Validate password confirmation
    form = ConfirmActionForm()
    if not form.validate_on_submit():
        flash("Password confirmation required.", "error")
        return redirect(url_for("iam.user", slug=slug))

    if not current_user.check_password(str(form.password.data)):
        flash("Incorrect password.", "error")
        return redirect(url_for("iam.user", slug=slug))

    # Prevent deleting yourself
    if user.id == current_user.id:
        flash("You cannot delete your own account.", "error")
        return redirect(url_for("iam.user", slug=slug))

    # Prevent deleting already deleted users
    if user.status == UserStatus.DELETED:
        flash("This account has already been deleted.", "warning")
        return redirect(url_for("iam.users"))

    username = user.profile.fullname if user.profile else user.username
    user.status = UserStatus.DELETED
    user.save()
    flash(f"Account for {username} has been deleted.", "success")
    return redirect(url_for("iam.users"))


@permission_required(IAMPermissions.VIEW_USERS)
def user_login_history_view(slug: str):
    """View user login history."""
    user = IAMUser.get_first_by(slug=slug)
    if not user:
        abort(404, description="User not found")

    # Get login history (already ordered by login_at desc via relationship)
    login_history = user.login_history

    display_name = user.profile.fullname if user.profile else user.username
    context = {
        "title": f"{display_name} - Login History",
        "user": user,
        "login_history": login_history,
        "back_url": url_for("iam.user", slug=slug),
        "breadcrumb": [
            {"url": url_for("iam.dashboard"), "label": "IAM"},
            {"url": url_for("iam.users"), "label": "Users"},
            {"url": url_for("iam.user", slug=slug), "label": display_name},
            {"url": None, "label": "Login History"},
        ],
    }
    return render_template("iam/user_login_history.html", **context)


@permission_required(IAMPermissions.VIEW_USERS)
def user_settings_view(slug: str):
    """View user settings and preferences."""
    user = IAMUser.get_first_by(slug=slug)
    if not user:
        abort(404, description="User not found")

    display_name = user.profile.fullname if user.profile else user.username
    context = {
        "title": f"{display_name} - Settings",
        "user": user,
        "back_url": url_for("iam.user", slug=slug),
        "breadcrumb": [
            {"url": url_for("iam.dashboard"), "label": "IAM"},
            {"url": url_for("iam.users"), "label": "Users"},
            {"url": url_for("iam.user", slug=slug), "label": display_name},
            {"url": None, "label": "Settings"},
        ],
    }
    return render_template("iam/user_settings.html", **context)


# =============================================================================
# Role Management Views
# =============================================================================


def roles_view():
    """Render the IAM Roles page."""
    context = {
        "title": "Roles",
        "breadcrumb": [
            {"url": url_for("iam.dashboard"), "label": "IAM"},
            {"url": None, "label": "Roles"},
        ],
    }
    return render_template("iam/roles.html", **context)


# =============================================================================
# Policies Management Views
# =============================================================================


def policies_view():
    """Render the IAM Policies page."""
    context = {
        "title": "Policies",
        "breadcrumb": [
            {"url": url_for("iam.dashboard"), "label": "IAM"},
            {"url": None, "label": "Policies"},
        ],
    }
    return render_template("iam/policies.html", **context)


# =============================================================================
# Permissions Management Views
# =============================================================================


def permissions_view():
    """Render the IAM Permissions page."""
    context = {
        "title": "Permissions",
        "breadcrumb": [
            {"url": url_for("iam.dashboard"), "label": "IAM"},
            {"url": None, "label": "Permissions"},
        ],
    }
    return render_template("iam/permissions.html", **context)


# =============================================================================
# Settings Management Views
# =============================================================================


def settings_view():
    """Render the IAM Settings page."""
    context = {
        "title": "Settings",
        "breadcrumb": [
            {"url": url_for("iam.dashboard"), "label": "IAM"},
            {"url": None, "label": "Settings"},
        ],
    }
    return render_template("iam/settings.html", **context)


# =============================================================================
# Authentication Views
# =============================================================================


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

        ip_address = request.remote_addr
        user_agent = request.headers.get("User-Agent")

        if user:
            if user.status == UserStatus.ACTIVE:
                login_user(user, remember=form.remember.data)
                user.record_login(ip_address=ip_address, user_agent=user_agent)
                flash(f"Welcome back {current_user.profile.fullname}.", "success")
                return redirect(url_for("main.dashboard"))

            # Record failed login due to account status
            user.record_login(
                ip_address=ip_address,
                user_agent=user_agent,
                is_successful=False,
                failure_reason=f"Account status: {user.status.value}",
            )

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


@login_required
def confirm_password_view():
    """Handle password confirmation for sensitive actions.

    This view is used as an intermediate step before allowing access
    to routes protected by @reauthenticate_required.
    """
    form = PasswordConfirmForm()
    next_url = request.args.get("next") or url_for("main.dashboard")

    # Validate next_url is safe (same host) to prevent open redirect
    if not is_safe_url(next_url):
        next_url = url_for("main.dashboard")

    if form.validate_on_submit():
        if current_user.check_password(str(form.password.data)):
            session[REAUTH_SESSION_KEY] = True
            return redirect(next_url)

        flash("Incorrect password. Please try again.", "error")

    context = {
        "title": "Confirm Password",
        "form": form,
        "next_url": next_url,
    }
    return render_template("iam/confirm_password.html", **context)
