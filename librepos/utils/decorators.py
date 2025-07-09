from functools import wraps

from flask import redirect, url_for
from flask_login import current_user

from librepos.utils import FlashMessageHandler


def permission_required(permission_name: str):
    """
    Decorator to restrict access to users with a specific permission.
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            if not current_user.is_authenticated:
                FlashMessageHandler.error("Authentication required.")
                return redirect(url_for("iam.auth.login"))

            if not current_user.has_permission(permission_name):
                FlashMessageHandler.error("You don't have the required permission.")
                return redirect(url_for("order.list_orders"))

            return view_func(*args, **kwargs)

        return wrapped_view

    return decorator
