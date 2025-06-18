from librepos.models import User
from .entity_repo import EntityRepository


class UserRepository(EntityRepository[User]):
    def __init__(self):
        super().__init__(User)

    @staticmethod
    def find_by_email(email: str) -> User | None:
        return User.query.filter_by(email=email).first()
