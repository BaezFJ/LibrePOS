from librepos.extensions import db
from librepos.models.restaurant import Restaurant


class MainRepository:
    @staticmethod
    def retrieve_restaurant():
        restaurant = Restaurant.query.get_or_404(1)
        return restaurant

    def update_restaurant(self, data):
        restaurant = self.retrieve_restaurant()
        if not restaurant:
            return None
        for key, value in data.items():
            setattr(restaurant, key, value)
        db.session.commit()
        return restaurant

    def get_restaurant_currency(self):
        restaurant = self.retrieve_restaurant()
        return restaurant.currency
