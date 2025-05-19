from librepos.models.users import User


class AuthRepository:
    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        return User.query.filter_by(email=email).first()
