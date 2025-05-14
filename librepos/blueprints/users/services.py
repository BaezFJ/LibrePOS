from librepos.extensions import db
from librepos.blueprints.auth.models import User
from librepos.blueprints.auth.repositories import UserRepository

from .repositories import ProfileRepository
from .models import UserProfile


class ProfileService:
    def __init__(self, profile_repo: ProfileRepository):
        self._profile_repo = profile_repo

    def get_profile(self, user_id: int) -> UserProfile:
        profile = self._profile_repo.get_by_user_id(user_id)
        if not profile:
            # create an empty profile if none exists
            profile = UserProfile(user_id=user_id)
            db.session.add(profile)
            db.session.commit()
        return profile

    def update_profile(self, user_id: int, data: dict) -> UserProfile:
        profile = self.get_profile(user_id)
        # for key, value in data.items():
        #     setattr(profile, key, value)
        # db.session.commit()
        # Only update allowed fields
        for field in ('first_name', 'middle_name', 'last_name', 'gender', 'marital_status', 'birthday', 'image'):
            if field in data:
                setattr(profile, field, data[field])
            db.session.commit()
        self._profile_repo.set_profile_image(user_id, data.get('image'))
        return profile


class UserService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def list_all_users(self) -> list[User] | None:
        return self._user_repo.list_users()

    def get_user(self, username: str) -> User | None:
        return self._user_repo.get_by_username(username)
