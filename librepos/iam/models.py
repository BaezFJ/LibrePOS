import secrets
from datetime import datetime
from enum import StrEnum
from typing import Optional

from flask_login import UserMixin
from slugify import slugify
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from librepos.extensions import AssociationModel, db
from librepos.utils.sqlalchemy import CRUDMixin


class UserStatus(StrEnum):
    ACTIVE = "active"
    PENDING = "pending"
    INVITED = "invited"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"
    LOCKED = "locked"
    DELETED = "deleted"


class UserGender(StrEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    NOT_SPECIFIED = "not_specified"


# User agent detection patterns: (keywords_to_match, result_value)
# Order matters - first match wins (e.g., Edge must come before Chrome)
_DEVICE_PATTERNS: list[tuple[tuple[str, ...], str]] = [
    (("mobile", "android", "iphone"), "Mobile"),
    (("tablet", "ipad"), "Tablet"),
]

_BROWSER_PATTERNS: list[tuple[tuple[str, ...], str]] = [
    (("firefox",), "Firefox"),
    (("edg",), "Edge"),
    (("chrome",), "Chrome"),
    (("safari",), "Safari"),
    (("opera", "opr"), "Opera"),
]

_OS_PATTERNS: list[tuple[tuple[str, ...], str]] = [
    (("windows",), "Windows"),
    (("mac os", "macos"), "macOS"),
    (("linux",), "Linux"),
    (("android",), "Android"),
    (("iphone", "ipad"), "iOS"),
]


def _match_ua_pattern(
    ua_lower: str,
    patterns: list[tuple[tuple[str, ...], str]],
    default: str,
) -> str:
    """Match user agent string against patterns, return first match or default."""
    for keywords, value in patterns:
        if any(kw in ua_lower for kw in keywords):
            return value
    return default


class IAMPermission(CRUDMixin, db.Model):
    __tablename__ = "iam_permission"
    # **************** Columns ****************
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    description: Mapped[str | None]

    # ************** Relationships ****************
    role_permissions: Mapped[list["IAMRolePermission"]] = relationship(
        foreign_keys=lambda: [IAMRolePermission.permission_id],
        back_populates="permission",
    )
    policy_permissions: Mapped[list["IAMPolicyPermission"]] = relationship(
        foreign_keys=lambda: [IAMPolicyPermission.permission_id],
        back_populates="permission",
    )

    @property
    def roles(self) -> list["IAMRole"]:
        """Get all roles that have this permission."""
        return [rp.role for rp in self.role_permissions]

    @property
    def policies(self) -> list["IAMPolicy"]:
        """Get all policies that have this permission."""
        return [pp.policy for pp in self.policy_permissions]

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name


class IAMPolicyPermission(CRUDMixin, AssociationModel):
    __tablename__ = "iam_policy_permission"
    # **************** Columns ****************
    policy_id: Mapped[int] = mapped_column(ForeignKey("iam_policy.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("iam_permission.id"), primary_key=True)
    added_by_id: Mapped[int | None] = mapped_column(ForeignKey("iam_user.id"), nullable=True)

    # **************** Relationships ****************
    added_by: Mapped[Optional["IAMUser"]] = relationship(foreign_keys=[added_by_id])
    policy: Mapped["IAMPolicy"] = relationship(back_populates="policy_permissions")
    permission: Mapped["IAMPermission"] = relationship(back_populates="policy_permissions")

    def __init__(self, policy_id: int, permission_id: int, **kwargs):
        super().__init__(**kwargs)
        self.policy_id = policy_id
        self.permission_id = permission_id


class IAMPolicy(CRUDMixin, db.Model):
    __tablename__ = "iam_policy"
    # **************** Columns ****************
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    description: Mapped[str | None]
    is_system: Mapped[bool] = mapped_column(default=False)

    # **************** Relationships ****************
    policy_permissions: Mapped[list["IAMPolicyPermission"]] = relationship(
        foreign_keys=lambda: [IAMPolicyPermission.policy_id],
        back_populates="policy",
    )
    role_policies: Mapped[list["IAMRolePolicy"]] = relationship(
        foreign_keys=lambda: [IAMRolePolicy.policy_id],
        back_populates="policy",
    )

    @property
    def permissions(self) -> list["IAMPermission"]:
        """Get all permissions in this policy."""
        return [pp.permission for pp in self.policy_permissions]

    @property
    def roles(self) -> list["IAMRole"]:
        """Get all roles that have this policy."""
        return [rp.role for rp in self.role_policies]

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.slug = slugify(name)


class IAMRolePermission(CRUDMixin, AssociationModel):
    __tablename__ = "iam_role_permission"
    # **************** Columns ****************
    role_id: Mapped[int] = mapped_column(ForeignKey("iam_role.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("iam_permission.id"), primary_key=True)
    added_by_id: Mapped[int | None] = mapped_column(ForeignKey("iam_user.id"), nullable=True)

    # **************** Relationships ****************
    added_by: Mapped[Optional["IAMUser"]] = relationship(foreign_keys=[added_by_id])
    role: Mapped["IAMRole"] = relationship(back_populates="role_permissions")
    permission: Mapped["IAMPermission"] = relationship(back_populates="role_permissions")

    def __init__(self, role_id: int, permission_id: int, **kwargs):
        super().__init__(**kwargs)
        self.role_id = role_id
        self.permission_id = permission_id


class IAMRolePolicy(CRUDMixin, AssociationModel):
    __tablename__ = "iam_role_policy"
    # **************** Columns ****************
    role_id: Mapped[int] = mapped_column(ForeignKey("iam_role.id"), primary_key=True)
    policy_id: Mapped[int] = mapped_column(ForeignKey("iam_policy.id"), primary_key=True)
    added_by_id: Mapped[int | None] = mapped_column(ForeignKey("iam_user.id"), nullable=True)

    # **************** Relationships ****************
    added_by: Mapped[Optional["IAMUser"]] = relationship(foreign_keys=[added_by_id])
    role: Mapped["IAMRole"] = relationship(back_populates="role_policies")
    policy: Mapped["IAMPolicy"] = relationship(back_populates="role_policies")

    def __init__(self, role_id: int, policy_id: int, **kwargs):
        super().__init__(**kwargs)
        self.role_id = role_id
        self.policy_id = policy_id


class IAMRole(CRUDMixin, db.Model):
    __tablename__ = "iam_role"
    # **************** Columns ****************
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    is_staff_role: Mapped[bool] = mapped_column(default=False)
    slug: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    description: Mapped[str | None]
    is_system: Mapped[bool] = mapped_column(default=False)

    # **************** Relationships ****************
    users: Mapped[list["IAMUser"]] = relationship(
        back_populates="role",
    )
    role_permissions: Mapped[list["IAMRolePermission"]] = relationship(
        foreign_keys=lambda: [IAMRolePermission.role_id],
        back_populates="role",
    )
    role_policies: Mapped[list["IAMRolePolicy"]] = relationship(
        foreign_keys=lambda: [IAMRolePolicy.role_id],
        back_populates="role",
    )

    @property
    def permissions(self) -> list["IAMPermission"]:
        """Get all permissions associated with this role (both direct and from policies)."""
        perms = [rp.permission for rp in self.role_permissions]
        for policy in self.policies:
            perms.extend(policy.permissions)
        return perms

    @property
    def policies(self) -> list["IAMPolicy"]:
        """Get all policies assigned to this role."""
        return [rp.policy for rp in self.role_policies]

    @classmethod
    def get_all_staff_roles(cls):
        """Get all staff roles."""
        return [role for role in cls.get_all() if role.is_staff_role]

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.slug = slugify(name)


class IAMUser(UserMixin, CRUDMixin, db.Model):
    __tablename__ = "iam_user"

    # **************** Foreign Keys ****************
    role_id: Mapped[int | None] = mapped_column(ForeignKey("iam_role.id"), nullable=True)

    # **************** Authentication Columns ****************
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(nullable=True)
    status: Mapped[UserStatus] = mapped_column(default=UserStatus.PENDING)
    verification_token: Mapped[str | None] = mapped_column(unique=True, index=True, nullable=True)

    # **************** Login Tracking Columns ****************
    login_count: Mapped[int] = mapped_column(default=0)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    current_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_login_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)

    # ************** Relationships ****************
    role: Mapped[Optional["IAMRole"]] = relationship(back_populates="users")
    profile: Mapped["IAMUserProfile"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    address: Mapped["IAMUserAddress"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    login_history: Mapped[list["IAMUserLoginHistory"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="desc(IAMUserLoginHistory.login_at)",
    )

    @property
    def is_staff(self) -> bool:
        return self.role.is_staff_role if self.role else False

    @property
    def permissions(self) -> list["IAMPermission"]:
        """Get all permissions from the user's role."""
        if self.role:
            return self.role.permissions
        return []

    def __init__(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        unsecure_password: str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.username = username
        self.slug = slugify(username)
        self.email = email

        if unsecure_password is not None:
            self.set_password(unsecure_password)

        # Auto-create a profile with personal information
        self.profile = IAMUserProfile(
            first_name=first_name,
            last_name=last_name,
        )

    def set_password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(str(self.hashed_password), password)

    def has_permission(self, permission_name: str) -> bool:
        """Check if the user has a given permission through their role.

        Args:
            permission_name: Name of the permission to check for

        Returns:
            bool: True if the user has the permission, False otherwise
        """
        return any(perm.name == permission_name for perm in self.permissions)

    def generate_verification_token(self) -> str:
        """Generate a secure verification token for passwordless registration.

        Returns:
            str: A URL-safe token string
        """
        token = secrets.token_urlsafe(32)
        self.verification_token = token
        return token

    def verify_token(self, token: str) -> bool:
        """Validate a verification token against the stored token.

        Args:
            token: The token to verify

        Returns:
            bool: True if the token matches, False otherwise
        """
        _token = str(self.verification_token)
        return self.verification_token is not None and secrets.compare_digest(_token, token)

    def clear_verification_token(self):
        """Clear the verification token after successful verification."""
        self.verification_token = None

    def record_login(
        self,
        ip_address: str | None = None,
        user_agent: str | None = None,
        is_successful: bool = True,
        failure_reason: str | None = None,
    ) -> "IAMUserLoginHistory":
        """Record a login attempt for this user.

        Args:
            ip_address: The IP address of the login attempt
            user_agent: The user agent string from the request
            is_successful: Whether the login was successful
            failure_reason: Reason for failure if unsuccessful

        Returns:
            IAMUserLoginHistory: The created login history record
        """
        now = datetime.utcnow()

        if is_successful:
            self.last_login_at = self.current_login_at
            self.current_login_at = now
            self.last_login_ip = ip_address
            self.login_count = (self.login_count or 0) + 1

        login_record = IAMUserLoginHistory(
            user_id=self.id,
            ip_address=ip_address,
            user_agent=user_agent,
            login_at=now,
            is_successful=is_successful,
            failure_reason=failure_reason,
        )
        login_record.save()

        if is_successful:
            self.save()

        return login_record


class IAMUserProfile(CRUDMixin, AssociationModel):
    __tablename__ = "iam_user_profile"

    # **************** Foreign Keys ****************
    user_id: Mapped[int] = mapped_column(ForeignKey("iam_user.id"), primary_key=True)

    # **************** Columns ****************
    first_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[str | None] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=False, default="default_profile_image.png")
    gender: Mapped[str | None] = mapped_column(
        nullable=True, default=UserGender.NOT_SPECIFIED.value
    )
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    date_of_birth: Mapped[str | None] = mapped_column(String(10), nullable=True)

    # ************** Relationships ****************
    user: Mapped["IAMUser"] = relationship(back_populates="profile", uselist=False)

    def __init__(self, first_name: str, last_name: str, **kwargs):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name

    @property
    def fullname(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"


class IAMUserAddress(CRUDMixin, AssociationModel):
    __tablename__ = "iam_user_address"

    # **************** Foreign Keys ****************
    user_id: Mapped[int] = mapped_column(ForeignKey("iam_user.id"), primary_key=True)

    # **************** Columns ****************
    address: Mapped[str | None] = mapped_column(nullable=False)
    city: Mapped[str | None] = mapped_column(nullable=False)
    state: Mapped[str | None] = mapped_column(nullable=False)
    country: Mapped[str | None] = mapped_column(nullable=False)
    zipcode: Mapped[str | None] = mapped_column(nullable=False)

    # ************** Relationships ****************
    user: Mapped["IAMUser"] = relationship(back_populates="address", uselist=False)

    @property
    def full_address(self) -> str:
        if self.address and self.city and self.state and self.country and self.zipcode:
            return f"{self.address}, {self.city}, {self.state}, {self.country} {self.zipcode}"
        return "Missing Address Information."


class IAMUserLoginHistory(CRUDMixin, db.Model):
    """Tracks detailed login history for users."""

    __tablename__ = "iam_user_login_history"

    # **************** Foreign Keys ****************
    user_id: Mapped[int] = mapped_column(ForeignKey("iam_user.id"), nullable=False, index=True)

    # **************** Login Details ****************
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)
    login_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    logout_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # **************** Login Status ****************
    is_successful: Mapped[bool] = mapped_column(default=True)
    failure_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # **************** Device Information ****************
    device_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    browser: Mapped[str | None] = mapped_column(String(100), nullable=True)
    os: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # **************** Geolocation (optional) ****************
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # ************** Relationships ****************
    user: Mapped["IAMUser"] = relationship(back_populates="login_history")

    def __init__(
        self,
        user_id: int,
        login_at: datetime,
        ip_address: str | None = None,
        user_agent: str | None = None,
        is_successful: bool = True,
        failure_reason: str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.login_at = login_at
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.is_successful = is_successful
        self.failure_reason = failure_reason

        if user_agent:
            self._parse_user_agent(user_agent)

    def _parse_user_agent(self, user_agent: str) -> None:
        """Parse user agent string to extract device, browser, and OS info."""
        ua_lower = user_agent.lower()
        self.device_type = _match_ua_pattern(ua_lower, _DEVICE_PATTERNS, "Desktop")
        self.browser = _match_ua_pattern(ua_lower, _BROWSER_PATTERNS, "Other")
        self.os = _match_ua_pattern(ua_lower, _OS_PATTERNS, "Other")

    def record_logout(self) -> None:
        """Record the logout time for this session."""
        self.logout_at = datetime.utcnow()
        self.save()

    @property
    def session_duration(self) -> str | None:
        """Calculate session duration if logout time is recorded."""
        if not self.logout_at:
            return None
        delta = self.logout_at - self.login_at
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{hours}h {minutes}m"
        if minutes > 0:
            return f"{minutes}m {seconds}s"
        return f"{seconds}s"
