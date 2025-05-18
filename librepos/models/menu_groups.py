from librepos.extensions import db
from librepos.utils import slugify_string


class MenuGroup(db.Model):
    """MenuGroup model."""

    __tablename__ = "menu_groups"

    def __init__(self, category_id: int, name: str, **kwargs):
        super(MenuGroup, self).__init__(**kwargs)
        """Create instance."""
        self.category_id = category_id
        self.name = name.capitalize()
        self.slug = slugify_string(name)

    # ForeignKeys
    category_id = db.Column(
        db.Integer, db.ForeignKey("menu_categories.id"), nullable=False
    )

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    # Relationships
    category = db.relationship("MenuCategory", back_populates="menu_groups")
    menu_items = db.relationship("MenuItem", back_populates="group")
