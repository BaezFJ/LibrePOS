from typing import List

from sqlalchemy.orm import Mapped, relationship

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime
from librepos.models.shop_orders import ShopOrder


class User(UserMixin, db.Model):
    """User model."""

    __tablename__ = "users"

    def __init__(
        self,
        first_name: str,
        middle_name: str | None,
        last_name: str,
        email: str,
        password: str,
        **kwargs,
    ):
        super(User, self).__init__(**kwargs)
        """Create instance."""
        self.first_name = first_name.title()
        self.middle_name = middle_name.title() if middle_name else None
        self.last_name = last_name.title()
        self.email = email.lower()
        self.password = generate_password_hash(password)
        self.created_at = timezone_aware_datetime()

        self.set_default_image()

    # ForeignKeys
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    active = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False)

    # Authentication
    password = db.Column(db.String(128), nullable=False)
    failed_login_count = db.Column(db.Integer, nullable=False, default=0)

    # Details
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    marital_status = db.Column(db.String(10), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    image = db.Column(db.String(255), nullable=True)

    # ContactInfo
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    phone = db.Column(db.String(15), nullable=True)
    phone_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)

    # ActivityTracking
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_on = db.Column(db.DateTime, nullable=True)
    current_sign_in_ip = db.Column(db.String(45), nullable=True)
    current_user_agent = db.Column(db.String(255), nullable=True)
    last_sign_in_on = db.Column(db.DateTime, nullable=True)
    last_sign_in_ip = db.Column(db.String(45), nullable=True)
    last_user_agent = db.Column(db.String(255), nullable=True)
    last_password_change = db.Column(db.DateTime, nullable=True)

    # Relationships
    role = db.relationship("Role", back_populates="users")
    orders: Mapped[List["ShopOrder"]] = relationship("ShopOrder", back_populates="user")

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}"

    def has_permission(self, permission_name: str) -> bool:
        if not self.role:
            return False
        return self.role.has_permission(permission_name)

    def set_default_image(self):
        if self.gender == "male":
            self.image = "images/default_male_user.png"

        if self.gender == "female":
            self.image = "images/default_female_user.png"

    def record_sign_in(self, ip: str, agent: str):
        self.sign_in_count += 1
        self.current_sign_in_on = timezone_aware_datetime()
        self.current_sign_in_ip = ip
        self.last_sign_in_on = self.current_sign_in_on
        self.last_sign_in_ip = self.current_sign_in_ip
        self.current_user_agent = agent
        self.last_user_agent = agent

        db.session.commit()

    def handle_failed_login(self):
        self.failed_login_count += 1
        if self.failed_login_count >= 3:
            self.active = False
        db.session.commit()

    def reset_failed_login_count(self):
        self.failed_login_count = 0
        db.session.commit()
