from functools import wraps

from flask import abort
from flask_login import current_user, login_required

from librepos.iam.models import UserStatus


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
