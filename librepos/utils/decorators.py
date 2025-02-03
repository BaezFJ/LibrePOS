from functools import wraps

from flask import redirect, request, url_for, flash
from flask_login import current_user

from librepos.utils.helpers import is_safe_url


def user_has_permission(permission: str):
    """
    Determines if the currently authenticated user has a specific permission.

    :param permission: Permission to check for the current user.
    :type permission: str
    :return: Boolean indicating whether the user has the specified permission.
    :rtype: bool
    """
    return hasattr(current_user, "role") and current_user.role.has_permission(permission)


def get_safe_redirect_url(default="dashboard.get_dashboard"):
    """
    Returns a safe redirect URL based on a user-provided "next" parameter. If the
    provided "next" URL is unsafe or absent, the function defaults to a specified
    fallback URL.

    The function ensures that user-provided input does not lead to unsafe
    redirects by validating the URL's safety using the `is_safe_url` function.
    Unsafe user input will be replaced with a secure default.

    :param default: Fallback route name to use if the provided URL is unsafe or
        not specified. Defaults to "dashboard.get_dashboard".
    :type default: str
    :return: A safe URL string for redirection.
    :rtype: str
    """
    next_url = request.args.get("next", "")
    next_url = next_url.replace("\\", "")
    if not next_url or not is_safe_url(next_url):
        next_url = url_for(default)
    return next_url


def permission_required(permission: str):
    """
    Decorator to restrict access to a route based on a user's permission. This decorator checks
    whether the current user holds the required permission before accessing the decorated function.
    If the user does not have the required permission, they will be flashed a message and redirected
    to a safe URL.

    This function takes a `permission` argument that specifies the permission string necessary to
    access the route.

    :param permission: The permission string required to access the decorated route
    :type permission: str
    :return: A decorator function that restricts access based on the specified permission
    :rtype: Callable
    """

    # TODO 2/3/25 : Fix bug where message gets send and put into the html content, but not rendering, could be an issue with MaterializeCSS.

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not user_has_permission(permission):
                flash("You don't have the appropriate permissions to access this page.", "danger")
                return redirect(get_safe_redirect_url())
            return f(*args, **kwargs)

        return decorated_function

    return decorator
