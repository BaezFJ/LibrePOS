from librepos.extensions import db
from librepos.utils.helpers import timezone_aware_datetime
from librepos.utils.sqlalchemy import CRUDMixin


class UserActivity(CRUDMixin, db.Model):
    # ForeignKeys
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)

    # Columns
    id = db.Column(db.Integer, primary_key=True, index=True)
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, nullable=False, default=0)
    last_ip_address = db.Column(db.String)
    device_info = db.Column(db.String)
    failed_login_attempts = db.Column(db.Integer, nullable=False, default=0)
    two_factor_enabled = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    user = db.relationship("User", back_populates="activity")

    def update_failed_login_attempts(self):
        if self.failed_login_attempts >= 3:
            from librepos.models.user import UserStatus

            self.user.change_status(UserStatus.LOCKED)
        self.failed_login_attempts += 1
        return self.save()

    def reset_failed_login_attempts(self):
        self.failed_login_attempts = 0
        return self.save()

    def update_activity(self, ip_address: str, device_info: str):
        self.login_count += 1
        self.last_login = timezone_aware_datetime()
        self.last_ip_address = ip_address
        self.device_info = device_info
        return self.save()
