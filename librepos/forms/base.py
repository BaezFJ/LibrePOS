# librepos/forms/base.py
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class BaseForm(FlaskForm):
    """Base form with common functionality"""
    pass


class ActiveEntityForm(BaseForm):
    """Base form for entities with active status"""
    active = BooleanField("Active", default=True)


class NamedEntityForm(ActiveEntityForm):
    """Base form for entities with name and active status"""
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={"placeholder": " "}
    )
