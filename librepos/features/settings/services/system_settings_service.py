from sqlalchemy.exc import SQLAlchemyError

from librepos.utils import FlashMessageHandler
from librepos.utils.model_utils import update_model_fields
from ..repositories import SystemSettingsRepository


class SystemSettingsService:
    def __init__(self):
        self.repository = SystemSettingsRepository()

    def get_system_settings(self):
        return self.repository.get_by_id(1)

    def update_system_settings(self, data):
        try:
            system_settings = self.repository.get_by_id(1)

            if not system_settings:
                FlashMessageHandler.error("System settings not found.")
                return None, False

            update_model_fields(system_settings, data)
            self.repository.update(system_settings)
            FlashMessageHandler.success("System settings updated successfully.")
            return system_settings, True

        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error updating system settings: {str(e)}")
            return None, False
