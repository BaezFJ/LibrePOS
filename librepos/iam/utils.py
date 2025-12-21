from typing import Optional
from sqlalchemy import or_

from librepos.extensions import db
from .models import IAMUser


def get_user_by_identifier(identifier: str) -> Optional[IAMUser]:
    """Find a user by username or email.

    Args:
        identifier: The username or email to search for

    Returns:
        IAMUser if found, None otherwise
    """
    user = db.session.execute(
        db.select(IAMUser).where(or_(IAMUser.username == identifier, IAMUser.email == identifier))
    ).scalar_one_or_none()

    return user


def authenticate_user(identifier: str, password: str) -> Optional[IAMUser]:
    """Authenticate a user by username/email and password.

    Args:
        identifier: The username or email
        password: The plaintext password to verify

    Returns:
        IAMUser if authentication succeeds, None otherwise
    """
    user = get_user_by_identifier(identifier)

    if user and user.check_password(password):
        return user

    return None
