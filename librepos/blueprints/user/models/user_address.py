from librepos.extensions import db
from librepos.utils.sqlalchemy import CRUDMixin


class UserAddress(CRUDMixin, db.Model):

    # ForeignKeys
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(50))
    postal_code = db.Column(db.String(20))
    gps_latitude = db.Column(db.Float)
    gps_longitude = db.Column(db.Float)
    is_default = db.Column(db.Boolean, default=False)
    
    # Relationships
    user = db.relationship("User", back_populates="addresses")
    