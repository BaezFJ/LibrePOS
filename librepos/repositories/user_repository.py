from librepos.extensions import db
from librepos.models.users import User


class UserRepository:
    @staticmethod
    def get_by_id(user_id: int) -> User | None:
        return User.query.get(user_id)

    @staticmethod
    def get_all() -> list[User]:
        return User.query.all()

    @staticmethod
    def find_by_email(email: str) -> User | None:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create(data) -> User:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user: User, **data) -> User:
        for key, val in data.items():
            setattr(user, key, val)
        db.session.commit()
        return user

    @staticmethod
    def delete(user: User) -> None:
        db.session.delete(user)
        db.session.commit()
