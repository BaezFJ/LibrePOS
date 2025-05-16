from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    description = StringField("Description", render_kw={"placeholder": " "})
    price = FloatField(
        "Price", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
