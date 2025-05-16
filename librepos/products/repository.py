from librepos.extensions import db
from librepos.models.products import Product


class ProductRepository:
    @staticmethod
    def get_all():
        return Product.query.order_by(Product.name).all()

    @staticmethod
    def get_by_id(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def create(data):
        product = Product(**data)
        db.session.add(product)
        db.session.commit()
        return product

    def update(self, product_id, data):
        product = self.get_by_id(product_id)
        if not product:
            return None
        for key, value in data.items():
            setattr(product, key, value)
        db.session.commit()
        return product

    def delete(self, product_id):
        product = self.get_by_id(product_id)
        if not product:
            return False
        db.session.delete(product)
        db.session.commit()
        return True
