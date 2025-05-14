from .models import User


class UserRepository:

    @staticmethod
    def get_by_username(username: str) -> User | None:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def list_users() -> list[User] | None:
        return User.query.order_by(User.username).all()
