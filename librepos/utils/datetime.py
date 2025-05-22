from datetime import datetime
from zoneinfo import ZoneInfo

from flask import current_app


def timezone_aware_datetime():
    timezone = current_app.config["TIMEZONE"]

    if not timezone:
        return datetime.now(ZoneInfo("UTC"))

    return datetime.now(ZoneInfo(timezone))
