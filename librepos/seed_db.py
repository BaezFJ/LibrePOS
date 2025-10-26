from librepos.features.iam.models import IAMPermission, IAMPermissionCategory
from librepos.features.iam.permissions import IAMPermissions
from librepos.main.extensions import db


def populate_permissions():
    """Seed the permission categories."""

    feature_permissions = [
        IAMPermissions,
    ]

    for feature in feature_permissions:
        new_category = IAMPermissionCategory(name=feature.__name__[:-11])
        db.session.add(new_category)
        db.session.commit()

        for permission in feature:
            # permission may be an Enum; get its name/description from value or attributes
            # Try value tuple first; fallback to attributes if defined.
            try:
                name, description = permission.value  # e.g., ("READ_USERS", "Can read users")
            except Exception:
                name = getattr(permission, "name", str(permission))
                description = getattr(permission, "description", "")

            feature_permission = IAMPermission(
                category_id=new_category.id,
                name=name,
                description=description,
            )
            db.session.add(feature_permission)
            db.session.commit()


def seed_all():
    populate_permissions()
