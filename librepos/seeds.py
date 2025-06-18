from librepos.extensions import db
from librepos.fixtures import ALL_PERMISSION_FIXTURES, ROLES_FIXTURE, POLICIES_FIXTURE
from librepos.models import (
    MenuCategory,
    MenuGroup,
    MenuItem,
    Permission,
    Policy,
    Restaurant,
    RolePolicy,
    Role,
    SystemSettings,
    User,
)


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


def seed_roles() -> None:
    all_roles = []
    for role in ROLES_FIXTURE:
        all_roles.extend([Role(name, description) for name, description in role])
    db.session.add_all(all_roles)
    db.session.commit()


def seed_permissions() -> None:
    all_permissions = []
    for permission_group in ALL_PERMISSION_FIXTURES:
        # Create the permission
        all_permissions.extend(
            [
                create_permission(name, description)
                for name, description in permission_group
            ]
        )
        db.session.add_all(all_permissions)
        db.session.commit()


def seed_policies() -> None:
    """Seed policies and their associated permissions."""
    from librepos.models import Permission, PolicyPermission

    all_policies = []

    for policy_name, policy_description, permission_names in POLICIES_FIXTURE:
        # Create the policy
        policy = Policy(policy_name, policy_description)
        all_policies.append(policy)
        db.session.add(policy)
        db.session.commit()

        # Add permissions to the policy
        for permission_name in permission_names:
            # Find the permission by name
            permission = Permission.query.filter_by(name=permission_name).first()

            if permission:
                # Create a policy-permission association
                policy_permission = PolicyPermission(
                    policy_id=policy.id,
                    permission_id=permission.id,
                    added_by="system",  # or whatever identifier you want to use
                )

                # Add to a database session
                db.session.add(policy_permission)
            else:
                # Log warning if permission doesn't exist
                print(
                    f"Warning: Permission '{permission_name}' not found for policy '{policy_name}'"
                )

    # Commit all policy-permission associations
    db.session.commit()


def seed_role_policies():
    admin_role = Role.query.filter_by(name="admin").first()

    if admin_role:
        # Get all policies that end with "_full"
        full_policies = Policy.query.filter(Policy.name.like("%_full")).all()

        # Add each full policy to an admin role
        for policy in full_policies:
            role_policy = RolePolicy(role_id=admin_role.id, policy_id=policy.id)
            db.session.add(role_policy)

        db.session.commit()

    manager_role = Role.query.filter_by(name="manager").first()
    if manager_role:
        # Get policies for managers
        manager_policies = [
            "user_management_limited",
            "role_management_view_only",
            "restaurant_settings_full",
        ]
        for policy_name in manager_policies:
            policy = Policy.query.filter_by(name=policy_name).first()
            if policy:
                role_policy = RolePolicy(role_id=manager_role.id, policy_id=policy.id)
                db.session.add(role_policy)
        db.session.commit()

    # Add the user_self_management_policy for all roles
    if admin_role and manager_role:
        user_self_management_policy = Policy.query.filter_by(
            name="user_self_management"
        ).first()
        if user_self_management_policy:
            for role in Role.query.all():
                self_management_role_policy = RolePolicy(
                    role_id=role.id, policy_id=user_self_management_policy.id
                )
                db.session.add(self_management_role_policy)
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

    seed_roles()
    seed_permissions()
    seed_policies()
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
