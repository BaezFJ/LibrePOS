from functools import wraps
from urllib.parse import urlparse, urlsplit

from flask import flash, redirect, request, url_for
from flask_login import current_user, login_required

from librepos.utils import safe_next_url


def permission_required(permission: str):
    """
    Check if the current user has the required permission to access a specific resource or perform an action.
    If the user does not have the necessary permission, they are redirected to the home page with a flash
    message.

    :param permission: The specific permission required for the user to access the resource or perform the action.
    :type permission: str
    :return: A decorator that applies the permission check to the decorated function.
    :rtype: Callable
    """

    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.role.has_permission(permission):
                next_url = request.args.get("next")
                if next_url:
                    next_url = next_url.replace("\\", "")
                if not next_url or urlsplit(next_url).netloc != "":
                    next_url = url_for("dashboard.get_dashboard")
                return redirect(next_url)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    """
    Decorator function to enforce admin-level access for a route or endpoint. This
    decorator ensures that the current user is authenticated and holds administrative
    permissions. It redirects non-admin users to the referring page or a default
    dashboard page with an appropriate flash message.

    :param f: The route handler function being decorated.
    :return: The decorated route handler function that enforces admin checks.
    """

    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.role.is_admin:
            next_url = request.args.get("next")
            if next_url:
                next_url = safe_next_url(next_url)
                flash("You do not have permission to do that.", "danger")
                return redirect(next_url)
            return redirect(url_for("user.get_dashboard"))
        return f(*args, **kwargs)

    return decorated_function
