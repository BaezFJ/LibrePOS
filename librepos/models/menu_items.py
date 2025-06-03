from librepos.extensions import db
from librepos.utils import slugify_string


class MenuItem(db.Model):
    """MenuItem model."""

    __tablename__ = "menu_items"

    def __init__(
        self, group_id: int, name: str, description: str, price: int, **kwargs
    ):
        super(MenuItem, self).__init__(**kwargs)
        """Create instance."""
        self.group_id = group_id
        self.name = name.title()
        self.slug = slugify_string(name)
        self.description = description.capitalize()
        self.price = price

    # ForeignKeys
    group_id = db.Column(db.Integer, db.ForeignKey("menu_groups.id"), nullable=False)

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Integer, nullable=False, default=0)
    active = db.Column(db.Boolean, nullable=False, default=True)

    # Relationships
    group = db.relationship("MenuGroup", back_populates="menu_items")

    @property
    def item_name_with_group(self):
        return f"{self.group.name} - {self.name}"
