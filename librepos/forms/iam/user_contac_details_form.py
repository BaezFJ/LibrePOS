from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class UserContactDetailsForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email()], render_kw={"placeholder": " "}
    )
    phone = StringField("Phone", render_kw={"placeholder": " "})
    address = StringField("Address", render_kw={"placeholder": " "})
    city = StringField("City", render_kw={"placeholder": " "})
    state = StringField("State", render_kw={"placeholder": " "})
    zipcode = StringField("Zipcode", render_kw={"placeholder": " "})
    country = StringField("Country", render_kw={"placeholder": " "})
    submit = SubmitField("Update Contact Details")
