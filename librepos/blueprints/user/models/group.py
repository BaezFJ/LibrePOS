from librepos.extensions import db
from librepos.utils.sqlalchemy import CRUDMixin, TimestampMixin


class Group(CRUDMixin, TimestampMixin, db.Model):
    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    # Relationship to join models
    policy_groups = db.relationship(
        "PolicyGroup", back_populates="group", cascade="all, delete-orphan"
    )
    group_users = db.relationship(
        "GroupUser", back_populates="group", cascade="all, delete-orphan"
    )

    @property
    def policies(self):
        return [pp.policy for pp in self.policy_groups]

    @property
    def users(self):
        return [gu.user for gu in self.group_users]
