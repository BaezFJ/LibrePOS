from functools import wraps

from flask import abort
from flask_login import current_user, login_required


def permission_required(permission: str):
    def decorator(func):
        @login_required
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.has_permission(permission):
                abort(403)

            return func(*args, **kwargs)

        return decorated_view

    return decorator
