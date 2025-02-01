from flask_login import login_user

from librepos.extensions import db
from librepos.utils.sqlalchemy import CRUDMixin
from librepos.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


def register_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        return False, "Username already exists."
    user = User(username=username, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return True, "User registered successfully."


def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first_or_404()
    if user and user.check_password(password):
        return user
    return None