from datetime import datetime
from zoneinfo import ZoneInfo


def timezone_aware_datetime(timezone: str = "America/New_York"):
    return datetime.now(ZoneInfo(timezone))
