from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from librepos.forms.base import BaseForm


class UserAddressForm(BaseForm):
    address = StringField(
        "Address", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    city = StringField(
        "City", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    state = StringField(
        "State", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    zipcode = StringField(
        "Zipcode", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    country = StringField(
        "Country", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    submit = SubmitField("Update Address")
