from librepos.extensions import db
from librepos.utils.helpers import timezone_aware_datetime
from librepos.utils.sqlalchemy import CRUDMixin


class RolePermission(CRUDMixin, db.Model):
    """Role-permission association."""

    def __init__(self, role_id, permission_id, **kwargs):
        super(RolePermission, self).__init__(**kwargs)
        self.role_id = role_id
        self.permission_id = permission_id

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    permission_id = db.Column(
        db.Integer, db.ForeignKey("permission.id"), nullable=False
    )
    assigned_date = db.Column(
        db.DateTime, nullable=False, default=lambda: timezone_aware_datetime()
    )
    assigned_by_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, default=0
    )

    # Relationships
    role = db.relationship("Role", back_populates="permissions")
    permission = db.relationship("Permission", back_populates="roles")
