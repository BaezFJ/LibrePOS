from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from librepos.extensions import db
from librepos.utils.helpers import (
    generate_uuid,
    generate_token,
    generate_slug,
    generate_password,
    dollars_to_cents,
)
from librepos.utils.sqlalchemy import CRUDMixin


class User(UserMixin, CRUDMixin, db.Model):

    def __init__(self, username, email, first_name, last_name, **kwargs):
        super(User, self).__init__(**kwargs)

        self.username = username
        self.slug = generate_slug(username)
        self.email = email
        self.public_id = generate_uuid()
        self.api_token = generate_token()
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()

        if kwargs.get("password_hash"):
            self.set_password(kwargs.get("password_hash"))
        else:
            temporary_password = generate_password()
            self.set_password(temporary_password)
            # TODO 1/28/25 : make a function to send the temporary password to user preferred method email/phone

            print(f"Temporary password for {username} is {temporary_password}")

    # ForeignKeys
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    slug = db.Column(db.String(30), unique=True, index=True)
    hourly_rate = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Authentication
    username = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    api_token = db.Column(db.String(128), unique=True, index=True)

    # Contact
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True)
    phone_number = db.Column(db.String(15), nullable=True, index=True)
    phone_number_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    role = db.relationship("Role", back_populates="users")
    orders = db.relationship("UserOrder", back_populates="user")

    @classmethod
    def get_by_identity(cls, identity: str):
        """Get a user by username or email."""
        return cls.query.filter((cls.username == identity) | (cls.email == identity))

    def set_password(self, password):
        """Set the user's password."""
        self.password_hash = generate_password_hash(
            password, salt_length=32, method="pbkdf2:sha256:80000"
        )

    def check_password(self, password):
        """Check if the user's password is correct."""
        return check_password_hash(self.password_hash, password)

    def in_role(self, role_name):
        """Check if the user is in the given role."""
        return self.role.name == role_name.lower()

    def check_role_permission(self, permission_name: str):
        """Check if the user has the given permission."""
        return self.role.has_permission(permission_name)

    def reset_password(self):
        """Reset the user's password."""
        if self.email_confirmed:
            token = generate_token()
            self.reset_token = token
            # TODO 1/26/25 : send token to the user's email to continue the password reset process.

        else:
            raise Exception("User is not confirmed.")

    def is_last_admin(self):
        """Check if the user is the last admin."""
        from librepos.models.role import Role

        admin_roles = Role.query.filter_by(is_admin=True).all()
        admin_count = 0
        for role in admin_roles:
            user_role_count = User.query.filter_by(role_id=role.id).count()
            admin_count += user_role_count
        return (
            self.role.is_admin
            and User.query.filter_by(role_id=self.role_id).count() == 1
            and admin_count == 1
        )

    def set_hourly_rate(self, new_rate):
        """Update the user's hourly rate."""
        self.hourly_rate = dollars_to_cents(new_rate)
        db.session.commit()
