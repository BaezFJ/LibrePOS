from typing import List

from librepos.extensions import db
from librepos.fixtures import ALL_PERMISSION_FIXTURES, ROLES_FIXTURE, POLICIES_FIXTURE
from librepos.models import (
    MenuCategory,
    MenuGroup,
    MenuItem,
    Permission,
    Policy,
    PolicyPermission,
    Restaurant,
    RolePolicy,
    Role,
    SystemSettings,
    User,
)


def create_permission(name: str, description: str) -> Permission:
    return Permission(name=name, description=description)


def create_role(name: str, description: str) -> Role:
    return Role(name=name, description=description)


def create_policy(name: str, description: str) -> Policy:
    return Policy(name=name, description=description)


def seed_system_settings():
    system_settings = SystemSettings(
        timezone="America/New_York",
        currency="USD",
        date_format="%m/%d/%Y",
        time_format="%I:%M %p",
        language="en",
        locale="en_US",
    )
    db.session.add(system_settings)
    db.session.commit()
    return system_settings


def seed_restaurant():
    restaurant = Restaurant(
        name="LibrePOS",
        address="123 Main St",
        city="New York",
        state="NY",
        zipcode="10001",
        country="USA",
        phone="9991234567",
        email="info@librepos.com",
        website="https://demo.librepos.com",
        currency="USD",
        timezone="America/New_York",
        tax_percentage="825",
    )
    db.session.add(restaurant)
    db.session.commit()
    return restaurant


def seed_roles() -> List[Role]:
    all_roles = []
    for role in ROLES_FIXTURE:
        all_roles.extend([create_role(name, description) for name, description in role])
    return all_roles


def seed_policies() -> List[Policy]:
    all_policies = []
    for policy in POLICIES_FIXTURE:
        all_policies.extend(
            [create_policy(name, description) for name, description in policy]
        )
    return all_policies


def seed_permissions() -> List[Permission]:
    all_permissions = []
    for permission_group in ALL_PERMISSION_FIXTURES:
        all_permissions.extend(
            [
                create_permission(name, description)
                for name, description in permission_group
            ]
        )
    return all_permissions


def seed_policy_permissions() -> None:
    permissions = Permission.query.all()
    admin_policy_permissions = permissions

    admin_policy = Policy.query.filter_by(name="administrator").first()

    if admin_policy:
        for permission in admin_policy_permissions:
            admin_policy_permission = PolicyPermission(
                policy_id=admin_policy.id,
                permission_id=permission.id,
                added_by="system",
            )
            db.session.add(admin_policy_permission)
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
    seed_restaurant()
    seed_system_settings()

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
