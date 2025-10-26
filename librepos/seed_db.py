from librepos.features.iam.permissions import IAMPermissions

from librepos.features.iam.models import IAMPermission
from librepos.main.extensions import db


def populate_iam_permissions():
    """Seed the iam permissions."""

    def _create_permission(name: str, description: str) -> IAMPermission:
        return IAMPermission(name, description)

    feature_permissions = [
        IAMPermissions,
    ]

    new_permissions = []

    for feature_permission in feature_permissions:
        for permission in feature_permission:
            new_permissions.append(_create_permission(permission.name, permission.description))

    db.session.add_all(new_permissions)
    db.session.commit()


def seed_all():
    populate_iam_permissions()
