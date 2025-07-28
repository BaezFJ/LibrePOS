from enum import StrEnum


class MenuPermissions(StrEnum):
    # Base access
    ACCESS = "menu.allow.access"

    # Category
    CREATE_CATEGORY = "menu.create.menu_category"
    READ_CATEGORY = "menu.read.menu_category"
    LIST_CATEGORY = "menu.list.menu_category"
    UPDATE_CATEGORY = "menu.update.menu_category"
    DELETE_CATEGORY = "menu.delete.menu_category"

    # Group
    CREATE_GROUP = "menu.create.menu_group"
    READ_GROUP = "menu.read.menu_group"
    LIST_GROUP = "menu.list.menu_group"
    UPDATE_GROUP = "menu.update.menu_group"
    DELETE_GROUP = "menu.delete.menu_group"

    # Item
    CREATE_ITEM = "menu.create.menu_item"
    READ_ITEM = "menu.read.menu_item"
    LIST_ITEM = "menu.list.menu_item"
    UPDATE_ITEM = "menu.update.menu_item"
    DELETE_ITEM = "menu.delete.menu_item"
