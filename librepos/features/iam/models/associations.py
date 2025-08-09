from librepos.extensions import db

__all__ = ["role_permission_association"]

role_permission_association = db.Table(
    "role_permission_association",
    db.metadata,
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column(
        "permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True
    ),
)
