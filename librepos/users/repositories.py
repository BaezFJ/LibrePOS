from librepos.extensions import db

from .models import UserProfile


class ProfileRepository:

    @staticmethod
    def get_by_user_id(user_id: int) -> UserProfile | None:
        return UserProfile.query.filter_by(user_id=user_id).first()
    
    def set_profile_image(self, user_id: int, image: str | None) -> None:
        profile = self.get_by_user_id(user_id)
        if profile is not None and image:
            profile.image = image
            db.session.commit()
        
