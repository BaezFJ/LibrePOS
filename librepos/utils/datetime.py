import importlib.resources
import os
from datetime import datetime
from zoneinfo import ZoneInfo


def timezone_aware_datetime():
    from librepos.repositories import SystemSettingsRepository

    timezone = SystemSettingsRepository().get_timezone()

    return datetime.now(ZoneInfo(timezone))


def get_all_timezones():
    """Return a sorted list of valid IANA time zone names."""
    VALID_REGION_PREFIXES = {
        "Africa",
        "America",
        "Antarctica",
        "Asia",
        "Atlantic",
        "Australia",
        "Europe",
        "Indian",
        "Pacific",
        "Etc",
        "UTC",
    }
    with importlib.resources.path("tzdata", "zoneinfo") as zoneinfo_dir:
        zones = []
        for root, _, files in os.walk(zoneinfo_dir):
            for file in files:
                if file == "__init__.py":
                    continue  # Skip __init__.py
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, zoneinfo_dir)
                zone_name = rel_path.replace(os.sep, "/")
                if "/" in zone_name and not zone_name.endswith(".py"):
                    if zone_name.split("/")[0] in VALID_REGION_PREFIXES:
                        zones.append(zone_name)
        return sorted(zones)
