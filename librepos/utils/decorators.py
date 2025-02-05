from functools import wraps

from flask import redirect, url_for, flash
from flask_login import current_user


def user_has_permission(permission: str) -> bool:
    """Check if the current user has the specified permission."""
    if not current_user:
        return False
    return current_user.has_permission(permission)


def permission_required(permission: str):
    """
    Decorator to restrict access to a route based on a user's permission.
    """

    def restrict_access(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_permission(permission):
                flash(
                    "You don't have the appropriate permissions to access this page.",
                    "danger",
                )
                return redirect(url_for("user.get_dashboard"))
            return f(*args, **kwargs)

        return decorated_function

    return restrict_access
