from librepos.extensions import db
from librepos.models.users import User


class UserRepository:
    @staticmethod
    def get_all():
        return User.query.order_by(User.last_name, User.first_name).all()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def create(data):
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user_id, data):
        user = self.get_by_id(user_id)
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True
