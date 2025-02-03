from functools import wraps

from flask import redirect, request, url_for, flash
from flask_login import current_user

from librepos.utils.helpers import is_safe_url


def permission_required(permission: str):
    """
    Decorator to enforce that the current user has the required permission to access
    a specific route or function. If the user lacks the required permission, they will
    be redirected to a safe URL, and an appropriate flash message will be displayed.

    The decorator checks the user's permission via their role and ensures that any
    passed "next" URL is safe before redirecting.

    :param permission: The specific permission required to access the wrapped route
        or function.
    :type permission: str
    :return: A decorated function that enforces the permission check.
    :rtype: Callable
    """

    # TODO 2/3/25 : Fix bug where message gets send and put into the html content, but not rendering, could be an issue with MaterializeCSS.

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.role.has_permission(permission):
                flash(f"You don't have the appropriate permissions to access this page.", "danger")
                next_url = request.args.get("next", "")
                next_url = next_url.replace("\\", "")  # In case backslashes might break parsing
                if not next_url or not is_safe_url(next_url):
                    next_url = url_for("dashboard.get_dashboard")
                return redirect(next_url)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
