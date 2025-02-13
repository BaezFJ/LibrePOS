import enum
from typing import cast, List, Any

from sqlalchemy import Enum

from librepos.extensions import db
from librepos.utils.sqlalchemy import CRUDMixin, TimestampMixin


class PolicyType(enum.Enum):
    SYSTEM = "system"
    CUSTOM = "custom"
    ALL = "all"


class Policy(CRUDMixin, TimestampMixin, db.Model):
    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    type = db.Column(Enum(PolicyType), nullable=False, default=PolicyType.SYSTEM)

    # Relationships to join models
    permission_policies = db.relationship(
        "PermissionPolicy", back_populates="policy", cascade="all, delete-orphan"
    )
    policy_groups = db.relationship(
        "PolicyGroup", back_populates="policy", cascade="all, delete-orphan"
    )

    @property
    def permissions(self) -> List[Any]:
        _permission_policies = cast(List[Any], self.permission_policies)
        return [pp.permission for pp in _permission_policies]

    @property
    def groups(self) -> List[Any]:
        _policy_groups = cast(List[Any], self.policy_groups)
        return [pg.group for pg in _policy_groups]
