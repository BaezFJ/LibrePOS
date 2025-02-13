from librepos.extensions import db
from librepos.utils.sqlalchemy import CRUDMixin, TimestampMixin


class GroupUser(CRUDMixin, TimestampMixin, db.Model):
    # ForeignKeys
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Relationships
    group = db.relationship("Group", back_populates="group_users")
    user = db.relationship("User", back_populates="group_users", foreign_keys=[user_id])
