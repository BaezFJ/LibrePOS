from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

from librepos.forms.base import BaseForm


class UserContactForm(BaseForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email()], render_kw={"placeholder": " "}
    )
    phone = StringField("Phone", render_kw={"placeholder": " "})
    submit = SubmitField("Update Contact")
