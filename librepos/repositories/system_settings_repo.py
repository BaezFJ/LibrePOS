from librepos.models.system_settings import SystemSettings

from . import EntityRepository


class SystemSettingsRepository(EntityRepository[SystemSettings]):
    def __init__(self):
        super().__init__(SystemSettings)

    def get_currency(self):
        settings = self.get_by_id(1)
        return settings.currency if settings else "USD"

    def get_timezone(self):
        settings = self.get_by_id(1)
        return settings.timezone if settings else "UTC"
