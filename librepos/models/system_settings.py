from sqlalchemy.orm import Mapped, mapped_column

from librepos.extensions import db


class SystemSettings(db.Model):
    """SystemSettings model."""

    __tablename__ = "system_settings"

    def __init__(
        self,
        timezone: str,
        currency: str,
        date_format: str,
        time_format: str,
        language: str,
        locale: str,
    ):
        super(SystemSettings, self).__init__()
        self.timezone = timezone
        self.currency = currency
        self.date_format = date_format
        self.time_format = time_format
        self.language = language
        self.locale = locale

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    timezone: Mapped[str]
    currency: Mapped[str]
    date_format: Mapped[str]
    time_format: Mapped[str]
    language: Mapped[str]
    locale: Mapped[str]
