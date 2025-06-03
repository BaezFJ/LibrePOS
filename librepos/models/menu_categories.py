from librepos.extensions import db
from librepos.utils import slugify_string


class MenuCategory(db.Model):
    """MenuCategory model."""

    __tablename__ = "menu_categories"

    def __init__(self, name: str, **kwargs):
        super(MenuCategory, self).__init__(**kwargs)
        self.name = name.capitalize()
        self.slug = slugify_string(name)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    # Relationships
    menu_groups = db.relationship("MenuGroup", back_populates="category")
