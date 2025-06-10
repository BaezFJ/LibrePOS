from librepos.repositories import SystemSettingsRepository


class SystemSettingsService:
    def __init__(self):
        self.repository = SystemSettingsRepository()

    def get_system_settings(self):
        return self.repository.get_by_id(1)
