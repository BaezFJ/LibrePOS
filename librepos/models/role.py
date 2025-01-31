from librepos.extensions import db
from librepos.utils.helpers import generate_slug
from librepos.utils.sqlalchemy import CRUDMixin


class Role(CRUDMixin, db.Model):

    def __init__(self, name, **kwargs):
        super(Role, self).__init__(**kwargs)

        self.name = name.lower()
        self.slug = generate_slug(name)

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.String(256), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_removable = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    users = db.relationship("User", back_populates="role")
    permissions = db.relationship("RolePermission", back_populates="role")

    def has_permission(self, permission_name):
        """Check if the role has the given permission."""
        from librepos.models.role_permission import RolePermission

        role_permission = RolePermission.query.filter_by(role_id=self.id).all()
        for rp in role_permission:
            if rp.permission.name == permission_name:
                return True
        return False

    @classmethod
    def get_active_roles(cls):
        return cls.query.filter_by(is_active=True).all()
