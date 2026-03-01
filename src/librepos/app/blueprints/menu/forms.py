"""WTForms for menu blueprint."""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    BooleanField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class MenuForm(FlaskForm):
    """Form for creating/editing menu."""

    submit = SubmitField("Submit")


class CategoryForm(FlaskForm):
    """Form for creating/editing categories."""

    name = StringField(
        "Category Name",
        validators=[DataRequired(), Length(max=100)],
        render_kw={"placeholder": "Enter category name..."},
    )
    description = TextAreaField(
        "Description",
        validators=[Optional(), Length(max=500)],
        render_kw={"placeholder": "Enter description (optional)..."},
    )
    parent_id = SelectField(
        "Parent Category",
        coerce=int,
        validators=[Optional()],
    )
    display_order = IntegerField(
        "Display Order",
        default=0,
        validators=[NumberRange(min=0)],
    )
    image = FileField(
        "Category Image",
        validators=[FileAllowed(["jpg", "jpeg", "png", "webp"])],
    )
    is_active = BooleanField("Active", default=True, render_kw={"render_as": "switch"})
