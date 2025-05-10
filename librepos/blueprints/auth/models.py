from librepos.extensions import db
from datetime import datetime
from zoneinfo import ZoneInfo


class Role(db.Model):
    """Role model."""

    __tablename__ = "roles"

    def __init__(self, name: str, description: str):
        super(Role, self).__init__()
        """Create instance."""
        self.name = name.lower()
        self.description = description.lower()

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(ZoneInfo("US/Central"))
    )
    active = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    users = db.relationship("User", back_populates="role")
    role_policies = db.relationship(
        "RolePolicy", back_populates="role", cascade="all, delete-orphan"
    )

    # policies = db.relationship('RolePolicy', back_populates='role', cascade='all, delete-orphan')

    def has_permission(self, permission_name: str) -> bool:
        """Check if any attached policy includes the permission."""
        for rp in self.role_policies:
            if rp.policy and rp.policy.has_permission(permission_name):
                return True
        return False


class Policy(db.Model):
    """Policy model."""

    __tablename__ = "policies"

    def __init__(self, name: str, description: str):
        super(Policy, self).__init__()
        """Create instance."""
        self.name = name.lower()
        self.description = description.lower()

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))

    # Relationships
    role_policies = db.relationship(
        "RolePolicy", back_populates="policy", cascade="all, delete-orphan"
    )
    policy_permissions = db.relationship(
        "PolicyPermission", back_populates="policy", cascade="all, delete-orphan"
    )

    # permissions = db.relationship('PolicyPermission', back_populates='policy', cascade='all, delete-orphan')

    def has_permission(self, permission_name: str) -> bool:
        return any(
            pp.permission.name == permission_name for pp in self.policy_permissions
        )


class Permission(db.Model):
    """Permission model."""

    __tablename__ = "permissions"

    def __init__(self, name: str, **kwargs):
        super(Permission, self).__init__(**kwargs)
        """Create instance."""
        self.name = name.lower()

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(ZoneInfo("US/Central"))
    )
    active = db.Column(db.Boolean, nullable=False, default=False)

    policy_permissions = db.relationship(
        "PolicyPermission", back_populates="permission", cascade="all, delete-orphan"
    )


# Association table with metadata: policy <-> permission
class PolicyPermission(db.Model):
    """PolicyPermission model: Association table with metadata: policy <-> permission"""

    __tablename__ = "policy_permissions"

    def __init__(self, policy_id: int, permission_id: int, added_by: str):
        super(PolicyPermission, self).__init__()
        """Create instance."""
        self.policy_id = policy_id
        self.permission_id = permission_id
        self.added_by = added_by.lower()

    # ForeignKeys
    policy_id = db.Column(db.Integer, db.ForeignKey("policies.id"), primary_key=True)
    permission_id = db.Column(
        db.Integer, db.ForeignKey("permissions.id"), primary_key=True
    )

    # Columns
    added_by = db.Column(db.String(64))
    added_at = db.Column(db.DateTime, default=datetime.now(ZoneInfo("US/Central")))

    # Relationships
    policy = db.relationship("Policy", back_populates="policy_permissions")
    permission = db.relationship("Permission", back_populates="policy_permissions")


# Association table with metadata: role <-> policy
class RolePolicy(db.Model):
    """RolePolicy model: Association table with metadata: role <-> policy"""

    __tablename__ = "role_policies"

    def __init__(self, role_id: int, policy_id: int, assigned_by: str):
        super(RolePolicy, self).__init__()
        """Create instance."""
        self.role_id = role_id
        self.policy_id = policy_id
        self.assigned_by = assigned_by.lower()

    # ForeignKeys
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey("policies.id"), primary_key=True)

    # Columns
    assigned_by = db.Column(db.String(64))
    assigned_at = db.Column(db.DateTime, default=datetime.now(ZoneInfo("US/Central")))

    # Relationships
    role = db.relationship("Role", back_populates="role_policies")
    policy = db.relationship("Policy", back_populates="role_policies")
