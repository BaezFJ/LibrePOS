"""Marshmallow schemas for menu blueprint."""

from marshmallow import Schema, fields  # pyright: ignore[reportMissingImports]


class MenuSchema(Schema):
    """Schema for serializing menu data."""

    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


# Schema instances
menu_schema = MenuSchema()
menus_schema = MenuSchema(many=True)
