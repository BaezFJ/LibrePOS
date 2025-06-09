from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class MenuCategoryForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    active = BooleanField("Active", default=True)
