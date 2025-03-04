from librepos.extensions import db
from librepos.utils.sqlalchemy import CRUDMixin, TimestampMixin


class MenuGroup(CRUDMixin, TimestampMixin, db.Model):
    """Menu groups are used to group menus."""

    # ForeignKeys
    parent_id = db.Column(db.Integer, db.ForeignKey("menu_group.id"), nullable=True)

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    visible = db.Column(db.Boolean, nullable=False, default=True)
    active = db.Column(db.Boolean, nullable=False, default=True)

    # Relationships
    parent = db.relationship("MenuGroup", remote_side="MenuGroup.id",
                             backref=db.backref("children", lazy="dynamic", cascade="all, delete-orphan"))
