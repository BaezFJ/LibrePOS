from enum import StrEnum


class SettingsPermissions(StrEnum):
    # Base access
    ACCESS = "settings.allow.access"

    READ_SETTINGS = "settings.read.settings"
    LIST_SETTINGS = "settings.list.settings"
    UPDATE_SETTINGS = "settings.update.settings"

    @property
    def description(self) -> str:
        return _DESCRIPTIONS[self]


_DESCRIPTIONS: dict[SettingsPermissions, str] = {
    SettingsPermissions.ACCESS: "View and navigate the System Settings interface for global configuration",
    SettingsPermissions.LIST_SETTINGS: "View and search through all system configuration settings",
    SettingsPermissions.READ_SETTINGS: "View detailed system setting configurations and current values",
    SettingsPermissions.UPDATE_SETTINGS: "Modify system-wide configuration settings and parameters",
}
