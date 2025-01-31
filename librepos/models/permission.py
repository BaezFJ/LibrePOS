from librepos.extensions import db
from librepos.utils.helpers import generate_slug
from librepos.utils.sqlalchemy import CRUDMixin


class Permission(CRUDMixin, db.Model):
    """Permissions are used to control access to certain resources."""

    def __init__(self, name, **kwargs):
        super(Permission, self).__init__(**kwargs)

        self.name = name.lower()
        self.slug = generate_slug(name)

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.String(256), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    roles = db.relationship("RolePermission", back_populates="permission")
