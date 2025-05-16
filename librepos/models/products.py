from slugify import slugify

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime


class Product(db.Model):
    """Product model."""

    __tablename__ = "products"

    def __init__(self, name: str, price: int, **kwargs):
        super(Product, self).__init__(**kwargs)
        self.name = name.capitalize()
        self.price = price
        self.slug = slugify(name, max_length=50, word_boundary=True)
        self.created_at = timezone_aware_datetime()

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
