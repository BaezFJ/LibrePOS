import enum

from sqlalchemy import Enum

from librepos.extensions import db
from librepos.utils.helpers import generate_uuid, timezone_aware_datetime
from librepos.utils.sqlalchemy import CRUDMixin, TimestampMixin


class TicketStatus(enum.Enum):
    OPEN = "open"
    VOIDED = "voided"
    WASTED = "wasted"
    CLOSED = "closed"


class PaymentStatus(enum.Enum):
    OPEN = "open"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class Ticket(CRUDMixin, TimestampMixin, db.Model):
    # ForeignKeys
    ticket_type_id = db.Column(db.Integer, db.ForeignKey("ticket_type.id"), nullable=False)

    # Columns
    id = db.Column(db.String(32), primary_key=True, index=True)
    ticket_status = db.Column(Enum(TicketStatus), nullable=False, default=TicketStatus.OPEN)
    payment_status = db.Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.OPEN)
    sequence_number = db.Column(db.Integer, nullable=False)

    # Relationships
    ticket_type = db.relationship("TicketType", back_populates="tickets")

    def __init__(self, **kwargs):
        super(Ticket, self).__init__(**kwargs)

        self.id = generate_uuid()
        self.sequencing_number = self.get_next_sequence_number()

    def get_next_sequence_number(self):
        """Get the next sequence number for this ticket."""
        today = timezone_aware_datetime().date()
        tickets_made_today = self.query.filter_by(created_date=today).all()
        next_sequence_number = (
            max([ticket.sequence_number for ticket in tickets_made_today]) + 1
            if tickets_made_today
            else 1
        )
        return next_sequence_number
