from librepos.models.users import User
from librepos.models.roles import Role
from librepos.models.permissions import Permission
from librepos.models.policies import Policy
from librepos.models.policy_permissions import PolicyPermission
from librepos.models.role_policies import RolePolicy
from librepos.models.menu_categories import MenuCategory
from librepos.models.menu_groups import MenuGroup
from librepos.models.menu_items import MenuItem

from librepos.extensions import db


def seed_roles():
    admin_role = Role(
        name="admin",
        description="Manage all aspects, including employee roles, menus, promotions, and settings.",
    )
    manager_role = Role(
        name="manager",
        description="Access to reports, inventory, and staff management (without system-level settings)",
    )
    cashier_role = Role(
        name="cashier",
        description="Process sales, apply discounts (if allowed), and issue receipts.  Limited access to reports (e.g., daily sales summary).",
    )
    waiter_role = Role(
        name="waiter",
        description="Enter orders, split bills, and send order tickets to kitchen printers or displays. Limited visibility of sales or reports.",
    )
    return [admin_role, manager_role, cashier_role, waiter_role]


def seed_policies():
    admin_policy = Policy(
        name="administrator", description="Allows full access to LibrePOS system."
    )
    manager_policy = Policy(
        name="manager",
        description="Limited access to reports, inventory, and staff management (without system-level settings)",
    )
    cashier_policy = Policy(
        name="cashier",
        description="Limited access to reports (e.g., daily sales summary).",
    )
    waiter_policy = Policy(
        name="waiter", description="Limited visibility of sales or reports."
    )
    return [admin_policy, manager_policy, cashier_policy, waiter_policy]


def seed_permissions():
    create_user_permission = Permission(
        name="create_user",
        description="Add user username, email, roles, and permissions",
    )
    get_user_permission = Permission(name="get_user", description="View user details")
    list_users_permission = Permission(
        name="list_users", description="View users and their roles"
    )
    update_user_permission = Permission(
        name="update_user",
        description="Edit user username, email, roles, and permissions",
    )
    delete_user_permission = Permission(
        name="delete_user", description="Delete user from system."
    )
    # MenuCategory Permissions
    create_menu_category = Permission(
        name="create_menu_category", description="Add category"
    )
    get_menu_category = Permission(
        name="get_menu_category", description="View category details"
    )
    list_menu_categories = Permission(
        name="list_menu_categories", description="View categories"
    )
    update_menu_category = Permission(
        name="update_menu_category", description="Edit category"
    )
    delete_menu_category = Permission(
        name="delete_menu_category", description="Delete category"
    )
    # MenuGroup Permissions
    create_menu_group = Permission(name="create_menu_group", description="Add group")
    get_menu_group = Permission(name="get_menu_group", description="View group details")
    list_menu_groups = Permission(name="list_menu_groups", description="View groups")
    update_menu_group = Permission(name="update_menu_group", description="Edit group")
    delete_menu_group = Permission(name="delete_menu_group", description="Delete group")

    # MenuItem Permissions
    create_menu_item = Permission(name="create_menu_item", description="Add item")
    get_menu_item = Permission(name="get_menu_item", description="View item details")
    list_menu_items = Permission(name="list_menu_items", description="View items")
    update_menu_item = Permission(name="update_menu_item", description="Edit item")
    delete_menu_item = Permission(name="delete_menu_item", description="Delete item")

    # Order Permissions
    create_order = Permission(name="create_order", description="Add order")
    get_order = Permission(name="get_order", description="View order details")
    list_orders = Permission(name="list_orders", description="View orders")
    update_order = Permission(name="update_order", description="Edit order")
    void_order = Permission(name="void_order", description="Void order")
    delete_order = Permission(name="delete_order", description="Delete order")

    return [
        create_user_permission,
        get_user_permission,
        list_users_permission,
        update_user_permission,
        delete_user_permission,
        create_menu_category,
        get_menu_category,
        list_menu_categories,
        update_menu_category,
        delete_menu_category,
        create_menu_group,
        get_menu_group,
        list_menu_groups,
        update_menu_group,
        delete_menu_group,
        create_menu_item,
        get_menu_item,
        list_menu_items,
        update_menu_item,
        delete_menu_item,
        create_order,
        get_order,
        list_orders,
        update_order,
        void_order,
        delete_order,
    ]


def seed_policy_permissions() -> None:
    permissions = Permission.query.all()
    admin_policy_permissions = permissions
    manager_policy_permissions = [
        p
        for p in permissions
        if p.name not in ["delete_user", "update_user", "create_user"]
    ]

    admin_policy = Policy.query.filter_by(name="administrator").first()
    manager_policy = Policy.query.filter_by(name="manager").first()

    if admin_policy:
        for permission in admin_policy_permissions:
            admin_policy_permission = PolicyPermission(
                policy_id=admin_policy.id,
                permission_id=permission.id,
                added_by="system",
            )
            db.session.add(admin_policy_permission)
            db.session.commit()

    if manager_policy:
        for permission in manager_policy_permissions:
            manager_policy_permission = PolicyPermission(
                policy_id=manager_policy.id,
                permission_id=permission.id,
                added_by="system",
            )
            db.session.add(manager_policy_permission)
            db.session.commit()


def seed_role_policies():
    admin_role = Role.query.filter_by(name="admin").first()
    admin_policy = Policy.query.filter_by(name="administrator").first()

    manager_role = Role.query.filter_by(name="manager").first()
    manger_policy = Policy.query.filter_by(name="manager").first()

    if admin_role and admin_policy:
        admin_role_policy = RolePolicy(
            role_id=admin_role.id, policy_id=admin_policy.id, assigned_by="system"
        )
        db.session.add(admin_role_policy)
        db.session.commit()

    if manager_role and manger_policy:
        manager_role_policy = RolePolicy(
            role_id=manager_role.id, policy_id=manger_policy.id, assigned_by="system"
        )
        db.session.add(manager_role_policy)
        db.session.commit()


def seed_users() -> None:
    admin_user = User(
        first_name="john",
        middle_name=None,
        last_name="doe",
        email="admin@librepos.com",
        password="librepos",
        gender="male",
        marital_status="married",
        phone="1234567890",
        active=True,
        role_id=1,
    )
    manager_user = User(
        first_name="jane",
        middle_name=None,
        last_name="doe",
        email="manager@librepos.com",
        password="librepos",
        gender="female",
        marital_status="married",
        phone="9991234567",
        active=True,
        role_id=2,
    )
    db.session.add_all(
        [
            admin_user,
            manager_user,
        ]
    )
    db.session.commit()


def load_menu_data():
    categories = ["Drinks", "Entrees", "Desserts"]
    drinks_groups = ["Can", "Bottle", "Hot"]
    items = [
        {
            "group_id": 1,
            "name": "Soda1",
            "description": "Soda 1 description",
            "price": 100,
        },
        {
            "group_id": 1,
            "name": "Soda2",
            "description": "Soda 2 description",
            "price": 150,
        },
    ]
    for category in categories:
        menu_category = MenuCategory(name=category)
        db.session.add(menu_category)
        db.session.commit()

    for group in drinks_groups:
        menu_group = MenuGroup(name=group, category_id=1)
        db.session.add(menu_group)
        db.session.commit()

    for item in items:
        menu_item = MenuItem(
            name=item["name"],
            description=item["description"],
            price=item["price"],
            group_id=item["group_id"],
        )
        db.session.add(menu_item)
        db.session.commit()


def seed_all():
    roles = seed_roles()
    policies = seed_policies()
    permissions = seed_permissions()

    db.session.add_all(permissions + list(roles) + policies)
    db.session.commit()

    seed_policy_permissions()
    seed_role_policies()
    seed_users()
    load_menu_data()


MENU_GROUPS = [
    {
        "name": "Entrees",
    },
    {
        "name": "Beverages",
    },
    {
        "name": "Desserts",
    },
]

TICKET_TYPES = [
    {"name": "dine-in", "icon": "table_restaurant"},
    {"name": "take-out", "icon": "takeout_dining", "default": True},
    {"name": "delivery", "icon": "delivery_dining", "active": False, "visible": False},
    {"name": "phone", "icon": "phone"},
    {"name": "drive-thru", "icon": "time_to_leave", "active": False, "visible": False},
    {"name": "online", "icon": "public", "visible": False},
]
