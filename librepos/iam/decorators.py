from functools import wraps

from flask import abort, redirect, request, session, url_for
from flask_login import current_user, login_required

from librepos.iam.models import UserStatus

REAUTH_SESSION_KEY = "_reauthenticated"


def reauthenticate_required(func):
    """Require password confirmation before accessing this route.

    This decorator redirects users to a password confirmation page
    before allowing access to sensitive operations.

    The session flag is consumed on POST requests (when actions are performed),
    but preserved on GET requests (when forms are rendered). This allows
    form-based views to render and submit without requiring re-confirmation.

    Example:
        @reauthenticate_required
        def reset_password_view():
            # Only accessible after password confirmation
            pass

        # Can be combined with permission_required:
        @permission_required('admin.delete_users')
        @reauthenticate_required
        def delete_user_view():
            pass
    """

    @login_required
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method == "POST":
            # POST: consume the key (one-time use for the action)
            if not session.pop(REAUTH_SESSION_KEY, False):
                next_url = request.url
                return redirect(url_for("iam.confirm_password", next=next_url))
        # GET: check but don't consume (form still needs to submit)
        elif not session.get(REAUTH_SESSION_KEY, False):
            next_url = request.url
            return redirect(url_for("iam.confirm_password", next=next_url))

        return func(*args, **kwargs)

    return decorated_view


def permission_required(permission: str):
    """Decorator to check if the current user has a specific permission.

    Args:
        permission: The name of the permission to check

    Returns:
        The decorated function if the user has permission, otherwise aborts with 403

    Example:
        @permission_required('user.create')
        def create_user():
            # Only users with 'user.create' permission can access this
            pass
    """

    def decorator(func):
        @login_required
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.status != UserStatus.ACTIVE:
                abort(403)

            if not current_user.has_permission(permission):
                abort(403)

            return func(*args, **kwargs)

        return decorated_view

    return decorator
