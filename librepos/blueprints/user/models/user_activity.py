from librepos.extensions import db
from librepos.utils.sqlalchemy import CRUDMixin


class UserActivity(CRUDMixin, db.Model):

    # ForeignKeys
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)

    # Columns
    id = db.Column(db.Integer, primary_key=True, index=True)
    last_login = db.Column(db.DateTime, nullable=False)
    last_ip_address = db.Column(db.String, nullable=False)
    device_info = db.Column(db.String, nullable=False)
    failed_login_attempts = db.Column(db.Integer, nullable=False, default=0)
    two_factor_enabled = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    user = db.relationship("User", back_populates="activity")


    def update_failed_login_attempts(self):
        self.failed_login_attempts += 1
    
    def reset_failed_login_attempts(self):
        self.failed_login_attempts = 0
