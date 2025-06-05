from sqlalchemy.exc import SQLAlchemyError
from librepos.utils.message_handlers import FlashMessageHandler

from .repository import MainRepository


class MainService:
    def __init__(self, repo=None):
        self.repo = repo or MainRepository()
        self.message_handler = FlashMessageHandler()

    def get_restaurant(self):
        return self.repo.retrieve_restaurant()

    def update_restaurant(self, data) -> bool:
        try:
            self.repo.update_restaurant(data)
            self.message_handler.success("Restaurant information updated successfully!")
            return True
        except SQLAlchemyError as e:
            self.message_handler.error("Error while updating restaurant information", e)
            return False
        except Exception as e:
            self.message_handler.error(
                "Unexpected error occurred while updating restaurant information", e
            )
            return False
