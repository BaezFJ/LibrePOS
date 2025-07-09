from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired

from librepos.utils.form import default_placeholder


class MenuCategoryForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired()], render_kw=default_placeholder
    )
    active = BooleanField("Active")
    submit = SubmitField("Add Category")
