from librepos.extensions import db
from librepos.utils.sqlalchemy import CRUDMixin, TimestampMixin


class PermissionPolicy(CRUDMixin, TimestampMixin, db.Model):
    # ForeignKeys
    permission_id = db.Column(
        db.Integer, db.ForeignKey("permission.id"), nullable=False
    )
    policy_id = db.Column(db.Integer, db.ForeignKey("policy.id"), nullable=False)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Relationships
    permission = db.relationship("Permission", back_populates="permission_policies")
    policy = db.relationship("Policy", back_populates="permission_policies")
