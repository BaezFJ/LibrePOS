from flask import flash

from .repository import ProductRepository


class ProductService:
    def __init__(self, repo=None):
        self.repo = repo or ProductRepository()

    def list_products(self):
        return self.repo.get_all()

    def get_product(self, product_id):
        return self.repo.get_by_id(product_id)

    def create_product(self, data):
        data["price"] = int(data["price"] * 100)
        return self.repo.create(data)

    def update_product(self, product_id, data):
        data["price"] = int(data["price"] * 100)
        flash("Product has been updated.", "success")
        return self.repo.update(product_id, data)
