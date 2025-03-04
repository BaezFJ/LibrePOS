from librepos.extensions import db
from librepos.utils.sqlalchemy import CRUDMixin


class TicketType(CRUDMixin, db.Model):
    """Ticket types are used to group tickets."""
    
    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    icon = db.Column(db.String(64), nullable=False, default="")
    visible = db.Column(db.Boolean, nullable=False, default=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    default = db.Column(db.Boolean, nullable=False, default=False)
    
    # Relationships
    tickets = db.relationship("Ticket", back_populates="ticket_type")
    