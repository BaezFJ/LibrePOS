from librepos.extensions import db
from librepos.features.branches.models import Branch
from librepos.features.iam.models import Role, User, Permission
from librepos.features.menu.models import MenuCategory, MenuGroup, MenuItem
from librepos.features.settings.models import SystemSettings
from .fixtures import ROLES_FIXTURE


def create_permission(name: str, description: str) -> Permission:
    return Permission(name=name, description=description)


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


def seed_branch():
    branch = Branch(
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
    db.session.add(branch)
    db.session.commit()
    return branch


def seed_roles() -> None:
    all_roles = []
    for role in ROLES_FIXTURE:
        all_roles.extend([Role(name, description) for name, description in role])
    db.session.add_all(all_roles)
    db.session.commit()


def seed_permissions() -> None:
    from librepos.features.iam.utils.enums import IAMPermissions
    from librepos.features.menu.utils.enums import MenuPermissions
    from librepos.features.branches.utils.enums import BranchPermissions
    from librepos.features.orders.utils.enums import OrderPermissions
    from librepos.features.settings.utils.enums import SettingsPermissions

    def _create_permission(
        permission_name: str, permission_description: str
    ) -> Permission:
        return Permission(name=permission_name, description=permission_description)

    feature_permissions = [
        IAMPermissions,
        MenuPermissions,
        BranchPermissions,
        OrderPermissions,
        SettingsPermissions,
    ]

    all_permissions = []

    for feature_permission in feature_permissions:
        for permission in feature_permission:
            all_permissions.append(
                _create_permission(permission, permission.description)
            )

    db.session.add_all(all_permissions)
    db.session.commit()


def seed_permissions_for_role() -> None:
    admin_role = Role.query.filter_by(name="admin").first()
    all_permissions = Permission.query.all()
    if admin_role:
        admin_role.permissions.extend(all_permissions)
        db.session.commit()
    return None


def seed_users() -> None:
    admin_user = User(
        username="admin",
        first_name="john",
        last_name="doe",
        email="admin@librepos.com",
        password="librepos",
        gender="male",
        marital_status="married",
        phone="1234567890",
        active=True,
        role_id=1,
        address="123 Main St",
        city="New York",
        state="NY",
        zipcode="10001",
        country="USA",
    )
    manager_user = User(
        username="manager",
        first_name="jane",
        last_name="doe",
        email="manager@librepos.com",
        password="librepos",
        gender="female",
        marital_status="married",
        phone="9991234567",
        active=True,
        role_id=2,
        address="123 Main St",
        city="New York",
        state="NY",
        zipcode="10001",
        country="USA",
    )
    db.session.add_all(
        [
            admin_user,
            manager_user,
        ]
    )
    db.session.commit()


def load_menu_data():
    categories = [
        {
            "name": "Beverages",
            "description": "Refreshing drinks, hot beverages and specialty drinks to complement your meal",
        },
        {
            "name": "Desserts",
            "description": "Indulge in our delectable selection of sweet treats and desserts made fresh daily",
        },
        {
            "name": "Entrees",
            "description": "Main course dishes featuring our chef's signature creations and house specialties",
        },
    ]
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
        menu_category = MenuCategory(
            name=category["name"], description=category["description"]
        )
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
    seed_branch()
    seed_system_settings()

    seed_roles()
    seed_permissions()
    seed_permissions_for_role()

    seed_users()
    load_menu_data()
