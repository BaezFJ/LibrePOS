from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField
from wtforms.validators import DataRequired

from librepos.utils.form import default_placeholder


class MenuCategoryForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired()], render_kw=default_placeholder
    )
    active = BooleanField("Active", default=True)
    submit = SubmitField("Add Category")
