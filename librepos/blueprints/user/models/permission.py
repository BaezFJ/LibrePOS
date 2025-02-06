from typing import List, cast, Any

from librepos.extensions import db
from librepos.utils.helpers import generate_slug
from librepos.utils.sqlalchemy import CRUDMixin


class Permission(CRUDMixin, db.Model):
    """Permissions are used to control access to certain resources."""

    def __init__(self, name, **kwargs):
        super(Permission, self).__init__(**kwargs)

        self.name = name
        self.slug = generate_slug(name)

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.String(256), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    # Relationship to the join model
    permission_policies = db.relationship(
        "PermissionPolicy", back_populates="permission", cascade="all, delete-orphan"
    )

    @property
    def policies(self) -> List[Any]:
        _policies = cast(List[Any], self.permission_policies)
        return [pp.policy for pp in _policies]
