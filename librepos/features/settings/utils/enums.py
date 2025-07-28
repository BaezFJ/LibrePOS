from enum import StrEnum


class SettingsPermissions(StrEnum):
    # Base access
    ACCESS = "settings.allow.access"

    READ_SETTINGS = "settings.read.settings"
    LIST_SETTINGS = "settings.list.settings"
    UPDATE_SETTINGS = "settings.update.settings"
