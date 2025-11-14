from librepos.features.iam.models import IAMPermission as IAMPermissionModel
from librepos.features.iam.models import IAMPermissionCategory
from librepos.features.iam.permissions import IAMPermission
from librepos.main.extensions import db


def populate_permissions():
    """Seed the permission categories."""
    feature_permissions = [
        IAMPermission,
    ]
    for feature in feature_permissions:
        # Extract category name
        category_name = feature.__name__.removesuffix("Permission")

        # Check if a category already exists
        existing_category = IAMPermissionCategory.query.filter_by(name=category_name).first()
        if existing_category:
            category = existing_category
        else:
            category = IAMPermissionCategory(name=category_name)
            db.session.add(category)
            db.session.flush()  # Get the ID without committing

        for permission in feature:
            # Check if permission already exists
            existing_permission = IAMPermissionModel.query.filter_by(name=permission.value).first()
            if existing_permission:
                continue

            # For StrEnum: permission.value is the string value, permission.description is a property
            feature_permission = IAMPermissionModel(
                category_id=category.id,
                name=permission.value,
                description=permission.description,
            )
            db.session.add(feature_permission)

        # Commit once per feature, not per permission
        db.session.commit()


def seed_all():
    populate_permissions()
