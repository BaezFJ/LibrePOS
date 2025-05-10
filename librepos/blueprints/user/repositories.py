from librepos.extensions import db

from .models import User, UserProfile


class UserRepository:

    # *** User Queries ***
    @staticmethod
    def get_by_username(username: str):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_id(user_id: int):
        return User.query.get(user_id)

    @staticmethod
    def get_all():
        return User.query.all()

    # *** Profile Queries ***
    @staticmethod
    def create_profile(user_id: int, **kwargs):
        profile = UserProfile(user_id=user_id, **kwargs)
        db.session.add(profile)
        return db.session.commit()

    @staticmethod
    def update_profile(user_id: int, **kwargs):
        profile = UserRepository.find_user_profile(user_id)
        if profile:
            for key, value in kwargs.items():
                setattr(profile, key, value)
            return db.session.commit()
        return UserRepository.create_profile(user_id, **kwargs)

    @staticmethod
    def find_user_profile(user_id: int):
        return UserProfile.query.filter_by(user_id=user_id).first()
