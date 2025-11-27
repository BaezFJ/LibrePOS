from librepos.features.iam.models import IAMPermission as IAMPermissionModel
from librepos.features.iam.models import IAMPermissionCategory
from librepos.features.iam.permissions import IAMPermission
from librepos.core.extensions import db
from librepos.features.iam.repositories import (
    IAMPermissionCategoryRepository,
    IAMPermissionRepository,
)


def populate_permissions():
    """Seed the permission categories."""
    category_repo = IAMPermissionCategoryRepository()
    permission_repo = IAMPermissionRepository()

    feature_permissions = [
        IAMPermission,
    ]

    for feature_enum in feature_permissions:
        # Extract category name
        category_name = feature_enum.__name__.removesuffix("Permission")

        # Get or create a category
        category = category_repo.get_by_field("name", category_name)
        if not category:
            category = category_repo.add(IAMPermissionCategory(name=category_name))

        for permission in feature_enum:
            # Check if permission already exists
            if permission_repo.get_by_field("name", permission.value):
                continue

            # For StrEnum: permission.value is the string value, permission.description is a property
            feature_permission = IAMPermissionModel(
                category_id=category.id,  # type: ignore
                name=permission.value,  # type: ignore
                description=permission.description,
            )
            db.session.add(feature_permission)

        # Commit once per feature
        db.session.commit()


def seed_all():
    populate_permissions()
