from functools import wraps
from typing import Any, Callable

from flask import redirect, url_for, request
from flask_login import login_required, current_user

from librepos.features.iam.repositories import IAMUserRepository
from librepos.utils import FlashMessageHandler

PERMISSION_DENIED_MESSAGE = "You don't have the required permission."
DEFAULT_UNAUTHORIZED_ENDPOINT = "core.home"

repo = IAMUserRepository()


def permission_required(
    permission: str, unauthorized_endpoint: str | None = None
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to restrict access to users with a specific permission.
    Authentication is enforced using Flask-Login's @login_required decorator.

    Args:
        permission: The required permission (string or StrEnum value).
        unauthorized_endpoint: Optional endpoint name to redirect to when the user
            lacks the required permission. If not provided, it falls back to
            DEFAULT_UNAUTHORIZED_ENDPOINT.

    Usage:
        @permission_required("iam.allow.access")
        def view(): ...

        # Or with a custom unauthorized redirect:
        @permission_required(IAMPermissions.CREATE_USER, unauthorized_endpoint="iam.user.unauthorized")
        def create_user(): ...
    """
    target_unauthorized_endpoint = (
        unauthorized_endpoint or DEFAULT_UNAUTHORIZED_ENDPOINT
    )

    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            if (
                not current_user.is_superuser
                or repo.group_has_permission(current_user, permission)
                or repo.user_has_permission(current_user, permission)
            ):
                FlashMessageHandler.error(PERMISSION_DENIED_MESSAGE)
                return redirect(url_for(target_unauthorized_endpoint, next=request.url))

            return view_func(*args, **kwargs)

        return wrapped_view

    return decorator
