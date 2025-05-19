from functools import wraps

from flask import redirect, url_for, flash
from flask_login import current_user


def permission_required(permission_name: str):
    """
    Decorator to restrict access to users with a specific permission.
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Authentication required to access this page.", "warning")
                return redirect(url_for("auth.login"))

            if not current_user.has_permission(permission_name):
                flash(
                    "You don't have the required permission to access this page. Contact a manager for assistance.",
                    "danger",
                )
                return redirect(url_for("dashboard.index"))

            return view_func(*args, **kwargs)

        return wrapped_view

    return decorator
