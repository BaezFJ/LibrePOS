from werkzeug.security import generate_password_hash

from librepos.extensions import db
from librepos.blueprints.user.models import User


def register_user(
    username: str, password: str, email: str, first_name: str, last_name: str
):
    user = User.query.filter_by(username=username).first()
    if user:
        return False, "Username already exists."
    user = User(
        username=username,
        password=generate_password_hash(password),
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    db.session.add(user)
    db.session.commit()
    return True, "User registered successfully."


def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first_or_404()
    if user and user.check_password(password):
        return user
    return None
