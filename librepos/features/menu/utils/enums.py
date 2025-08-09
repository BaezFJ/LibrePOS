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

    @property
    def description(self) -> str:
        return _DESCRIPTIONS[self]


_DESCRIPTIONS: dict[MenuPermissions, str] = {
    MenuPermissions.ACCESS: "View and navigate the Menu Management interface for configuring restaurant menus",
    MenuPermissions.CREATE_CATEGORY: "Create new menu categories to organize menu items (e.g. Appetizers, Entrees)",
    MenuPermissions.READ_CATEGORY: "View detailed menu category information including description and contained items",
    MenuPermissions.LIST_CATEGORY: "View and search through all menu categories and their organizational structure",
    MenuPermissions.UPDATE_CATEGORY: "Modify existing menu category details including name, description and organization",
    MenuPermissions.DELETE_CATEGORY: "Permanently remove menu categories and reassign or delete contained items",
    MenuPermissions.CREATE_GROUP: "Create new menu groups within categories for further menu organization",
    MenuPermissions.READ_GROUP: "View detailed menu group information including contained items and category assignment",
    MenuPermissions.LIST_GROUP: "View and search through all menu groups and their organizational structure",
    MenuPermissions.UPDATE_GROUP: "Modify existing menu group details including name, category and organization",
    MenuPermissions.DELETE_GROUP: "Permanently remove menu groups and reassign or delete contained items",
    MenuPermissions.CREATE_ITEM: "Add new menu items with pricing, descriptions and category/group assignments",
    MenuPermissions.READ_ITEM: "View detailed menu item information including pricing, descriptions and availability",
    MenuPermissions.LIST_ITEM: "View and search through all menu items across categories and groups",
    MenuPermissions.UPDATE_ITEM: "Modify existing menu item details including pricing, descriptions and assignments",
    MenuPermissions.DELETE_ITEM: "Permanently remove menu items from the system",
}
