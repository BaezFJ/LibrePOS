from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo


def fetch_time_by_timezone(timezone: str = "America/New_York"):
    return datetime.now(ZoneInfo(timezone))


def timedelta_months(months, compare_date=None):
    """
    Return a new datetime with a month offset applied.

    :param months: Number of months to offset
    :type months: int
    :param compare_date: Date to compare at
    :type compare_date: date
    :return: datetime
    """
    if compare_date is None:
        compare_date = date.today()

    delta = months * 365 / 12
    return compare_date + timedelta(delta)
