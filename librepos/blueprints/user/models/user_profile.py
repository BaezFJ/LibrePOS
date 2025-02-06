from librepos.extensions import db
from librepos.utils.sqlalchemy import CRUDMixin


class UserProfile(CRUDMixin, db.Model):
    # ForeignKeys
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    profile_picture = db.Column(db.String(255))
    bio = db.Column(db.Text)
    language = db.Column(db.String(5))
    timezone = db.Column(db.String(50))
    dark_mode_enabled = db.Column(db.Boolean, default=False)

    # Relationships
    user = db.relationship("User", back_populates="profile")

    @property
    def full_name(self) -> str:
        return str(self.first_name + " " + self.last_name)
