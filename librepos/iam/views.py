from datetime import datetime, timedelta

from flask import abort, current_app, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from librepos.extensions import db
from librepos.utils.export import ExportField, export_to_csv
from librepos.utils.images import delete_user_image, process_user_image
from librepos.utils.navigation import get_redirect_url, is_safe_url
from librepos.utils.pagination import paginate_query

from .decorators import REAUTH_SESSION_KEY, permission_required, reauthenticate_required
from .email import send_invitation_email, send_password_reset_email, send_welcome_email
from .forms import (
    AdminResetPasswordForm,
    ConfirmActionForm,
    ForgotPasswordForm,
    PasswordConfirmForm,
    SetPasswordForm,
    UserAddressForm,
    UserEditForm,
    UserImageForm,
    UserLoginForm,
    UserProfileForm,
    UserRegisterForm,
)
from .models import (
    IAMPermission,
    IAMPolicy,
    IAMRole,
    IAMUser,
    IAMUserAddress,
    IAMUserProfile,
    UserStatus,
)
from .permissions import IAMPermissions
from .queries import (
    failed_logins_query,
    latest_login_per_user_query,
    users_count_by_role,
    users_list_query,
)
from .utils import authenticate_user, get_user_by_identifier

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

_iam_dashboard = "iam.dashboard"


def dashboard_view():
    """Render the IAM dashboard with statistics."""
    # User statistics
    total_users = IAMUser.query.count()
    active_users = IAMUser.query.filter_by(status=UserStatus.ACTIVE).count()
    locked_users = IAMUser.query.filter_by(status=UserStatus.LOCKED).count()
    pending_users = IAMUser.query.filter_by(status=UserStatus.PENDING).count()

    # Role/Permission statistics
    total_roles = IAMRole.query.count()
    total_policies = IAMPolicy.query.count()
    total_permissions = IAMPermission.query.count()

    # Security statistics (failed logins in last 24h)
    yesterday = datetime.now() - timedelta(days=1)
    failed_logins = failed_logins_query(yesterday).count()

    # Recent activity - latest login per user (paginated)
    login_query = latest_login_per_user_query()
    login_pagination = paginate_query(login_query, per_page=5)

    # Users by role
    users_by_role = users_count_by_role()
    context = {
        "title": "IAM Dashboard",
        # User stats
        "total_users": total_users,
        "active_users": active_users,
        "locked_users": locked_users,
        "pending_users": pending_users,
        # Role/Perm stats
        "total_roles": total_roles,
        "total_policies": total_policies,
        "total_permissions": total_permissions,
        # Security
        "failed_logins_24h": failed_logins,
        "recent_logins": login_pagination.items,
        "login_pagination": login_pagination,
        # Distribution
        "users_by_role": users_by_role,
    }
    return render_template("iam/dashboard.html", **context)


def dashboard_activity_view():
    """Return paginated activity table partial for HTMX requests."""
    login_query = latest_login_per_user_query()
    login_pagination = paginate_query(login_query, per_page=5)

    return render_template(
        "iam/_activity_table.html",
        recent_logins=login_pagination.items,
        login_pagination=login_pagination,
    )


# =============================================================================
# User Management Views
# =============================================================================


@permission_required(IAMPermissions.VIEW_USERS)
def users_view():
    """Render the IAM Users page."""
    form = UserRegisterForm(current_user=current_user)

    # Handle search, filter, and sort
    search_query = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "")
    sort_field = request.args.get("sort", "username")

    query = users_list_query(
        search=search_query or None,
        status=status_filter or None,
        sort=sort_field,
    )
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
            {"url": url_for(_iam_dashboard), "label": "IAM"},
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
            {"url": url_for(_iam_dashboard), "label": "IAM"},
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
            {"url": url_for(_iam_dashboard), "label": "IAM"},
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
            {"url": url_for(_iam_dashboard), "label": "IAM"},
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
            {"url": url_for(_iam_dashboard), "label": "IAM"},
            {"url": url_for("iam.users"), "label": "Users"},
            {"url": url_for("iam.user", slug=slug), "label": display_name},
            {"url": None, "label": "Address"},
        ],
    }
    return render_template("iam/user_address.html", **context)


@permission_required(IAMPermissions.CREATE_USERS)
def add_user_view():
    """Render standalone user creation page with invitation flow."""
    form = UserRegisterForm(current_user=current_user)

    if form.validate_on_submit():
        # Create user with INVITED status (no password)
        user = IAMUser(
            username=str(form.username.data),
            email=str(form.email.data),
            first_name=str(form.first_name.data),
            last_name=str(form.last_name.data),
            role_id=form.role_id.data,
        )
        user.status = UserStatus.INVITED

        # Generate verification token
        token = user.generate_verification_token()
        user.save()

        # Send invitation email
        email_sent = send_invitation_email(user, token)

        if email_sent:
            flash(
                f"User {user.profile.fullname} created successfully. "
                f"An invitation email has been sent to {user.email}.",
                "success",
            )
        else:
            flash(
                f"User {user.profile.fullname} created, but the invitation email "
                f"could not be sent. You may need to resend the invitation.",
                "warning",
            )

        return redirect(url_for("iam.user", slug=user.slug))

    context = {
        "title": "Add User",
        "form": form,
        "breadcrumb": [
            {"url": url_for(_iam_dashboard), "label": "IAM"},
            {"url": url_for("iam.users"), "label": "Users"},
            {"url": None, "label": "Add User"},
        ],
    }
    return render_template("iam/add_user.html", **context)


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
            {"url": url_for(_iam_dashboard), "label": "IAM"},
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
            {"url": url_for(_iam_dashboard), "label": "IAM"},
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
            {"url": url_for(_iam_dashboard), "label": "IAM"},
            {"url": url_for("iam.users"), "label": "Users"},
            {"url": url_for("iam.user", slug=slug), "label": display_name},
            {"url": None, "label": "Settings"},
        ],
    }
    return render_template("iam/user_settings.html", **context)


# =============================================================================
# Invitation Views
# =============================================================================


def accept_invitation_view(token: str):
    """Handle invitation acceptance and password setup.

    This view is public (no login required) - user sets password here.
    """
    # Find user by verification token
    user = IAMUser.get_first_by(verification_token=token)

    if not user:
        flash("Invalid or expired invitation link.", "error")
        return redirect(url_for("iam.login"))

    # Verify user is in INVITED status
    if user.status != UserStatus.INVITED:
        flash(
            "This invitation has already been used or the account is not in invited status.",
            "warning",
        )
        return redirect(url_for("iam.login"))

    form = SetPasswordForm()

    if form.validate_on_submit():
        # Set password and activate account
        user.set_password(str(form.password.data))
        user.status = UserStatus.ACTIVE
        user.clear_verification_token()
        user.save()

        # Send welcome email (optional, best effort)
        send_welcome_email(user)

        flash(
            "Your password has been set successfully. You can now log in.",
            "success",
        )
        return redirect(url_for("iam.login"))

    context = {
        "title": "Accept Invitation",
        "form": form,
        "user": user,
    }
    return render_template("iam/accept_invitation.html", **context)


@permission_required(IAMPermissions.EDIT_USERS)
def resend_invitation_view(slug: str):
    """Resend invitation email to a user in INVITED status."""
    user = IAMUser.get_first_by(slug=slug)

    if not user:
        flash("User not found.", "error")
        return redirect(url_for("iam.users"))

    if user.status != UserStatus.INVITED:
        flash("Can only resend invitations to users with 'Invited' status.", "warning")
        return redirect(url_for("iam.user", slug=slug))

    # Generate new token (invalidates old one)
    token = user.generate_verification_token()
    user.save()

    # Send invitation email
    email_sent = send_invitation_email(user, token)

    if email_sent:
        flash(f"Invitation email has been resent to {user.email}.", "success")
    else:
        flash("Failed to send invitation email. Please try again.", "error")

    return redirect(url_for("iam.user", slug=slug))


# =============================================================================
# Role Management Views
# =============================================================================


def roles_view():
    """Render the IAM Roles page."""
    context = {
        "title": "Roles",
        "breadcrumb": [
            {"url": url_for(_iam_dashboard), "label": "IAM"},
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
            {"url": url_for(_iam_dashboard), "label": "IAM"},
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
            {"url": url_for(_iam_dashboard), "label": "IAM"},
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
            {"url": url_for(_iam_dashboard), "label": "IAM"},
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


def forgot_password_view():
    """Handle forgot password requests.

    This view is public (no login required). User enters username or email,
    and if found with ACTIVE status, receives a password reset email.
    Always shows success message to prevent user enumeration.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = ForgotPasswordForm()

    if form.validate_on_submit():
        identifier = str(form.identifier.data).strip()
        user = get_user_by_identifier(identifier)

        # Only send email if user exists and is ACTIVE
        if user and user.status == UserStatus.ACTIVE:
            token = user.generate_verification_token()
            user.save()
            send_password_reset_email(user, token)

        # Always show same message to prevent user enumeration
        flash(
            "If an account exists with that username or email, "
            "a password reset link has been sent.",
            "info",
        )
        return redirect(url_for("iam.login"))

    context = {
        "title": "Forgot Password",
        "form": form,
    }
    return render_template("iam/forgot_password.html", **context)


def reset_password_view(token: str):
    """Handle password reset via token.

    This view is public (no login required). User clicks link from email
    and sets a new password.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    # Find user by verification token
    user = IAMUser.get_first_by(verification_token=token)

    if not user:
        flash("Invalid or expired password reset link.", "error")
        return redirect(url_for("iam.login"))

    # Verify token is still valid (not expired)
    if not user.verify_token(token):
        flash("This password reset link has expired. Please request a new one.", "error")
        return redirect(url_for("iam.forgot_password"))

    # Only allow reset for ACTIVE users
    if user.status != UserStatus.ACTIVE:
        flash("Unable to reset password for this account. Please contact support.", "error")
        return redirect(url_for("iam.login"))

    form = SetPasswordForm()

    if form.validate_on_submit():
        user.set_password(str(form.password.data))
        user.clear_verification_token()
        user.save()

        flash("Your password has been reset successfully. You can now log in.", "success")
        return redirect(url_for("iam.login"))

    context = {
        "title": "Reset Password",
        "form": form,
        "user": user,
    }
    return render_template("iam/reset_password_token.html", **context)


@login_required
def confirm_password_view():
    """Handle password confirmation for sensitive actions.

    This view is used as an intermediate step before allowing access
    to routes protected by @reauthenticate_required.
    """
    form = PasswordConfirmForm()
    requested_next = request.args.get("next")
    if requested_next and is_safe_url(requested_next):
        next_url = requested_next
    else:
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
