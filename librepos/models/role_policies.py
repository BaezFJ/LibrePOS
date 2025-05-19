from librepos.extensions import db
from librepos.utils import timezone_aware_datetime


# Association table with metadata: role <-> policy
class RolePolicy(db.Model):
    """RolePolicy model: Association table with metadata: role <-> policy"""

    __tablename__ = "role_policies"

    def __init__(self, role_id: int, policy_id: int, assigned_by: str):
        super(RolePolicy, self).__init__()
        """Create instance."""
        self.role_id = role_id
        self.policy_id = policy_id
        self.assigned_by = assigned_by.lower()
        self.assigned_at = timezone_aware_datetime()

    # ForeignKeys
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey("policies.id"), primary_key=True)

    # Columns
    assigned_by = db.Column(db.String(64))
    assigned_at = db.Column(db.DateTime)

    # Relationships
    role = db.relationship("Role", back_populates="role_policies")
    policy = db.relationship("Policy", back_populates="role_policies")
