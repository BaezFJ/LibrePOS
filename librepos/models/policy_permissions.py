from librepos.extensions import db
from librepos.utils import timezone_aware_datetime


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
        self.added_at = timezone_aware_datetime()

    # ForeignKeys
    policy_id = db.Column(db.Integer, db.ForeignKey("policies.id"), primary_key=True)
    permission_id = db.Column(
        db.Integer, db.ForeignKey("permissions.id"), primary_key=True
    )

    # Columns
    added_by = db.Column(db.String(64))
    added_at = db.Column(db.DateTime)

    # Relationships
    policy = db.relationship("Policy", back_populates="policy_permissions")
    permission = db.relationship("Permission", back_populates="policy_permissions")
