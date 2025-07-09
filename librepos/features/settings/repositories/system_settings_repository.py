from librepos.common.base_repository import BaseRepository

from ..models import SystemSettings


class SystemSettingsRepository(BaseRepository[SystemSettings]):
    def __init__(self):
        super().__init__(SystemSettings)

    def get_currency(self):
        settings = self.get_by_id(1)
        return settings.currency if settings else "USD"

    def get_timezone(self):
        settings = self.get_by_id(1)
        return settings.timezone if settings else "UTC"

    def get_locale(self):
        settings = self.get_by_id(1)
        return settings.locale if settings else "en_US"

    def get_date_format(self):
        settings = self.get_by_id(1)
        return settings.date_format if settings else "YYYY-MM-DD"

    def get_time_format(self):
        settings = self.get_by_id(1)
        return settings.time_format if settings else "HH:mm"
