from librepos.extensions import db
from librepos.utils.sqlalchemy import CRUDMixin, TimestampMixin


class PolicyGroup(CRUDMixin, TimestampMixin, db.Model):
    """Policy groups are used to group policies."""

    # ForeignKeys
    policy_id = db.Column(db.Integer, db.ForeignKey("policy.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=False)

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Relationships
    policy = db.relationship("Policy", back_populates="policy_groups")
    group = db.relationship("Group", back_populates="policy_groups")
