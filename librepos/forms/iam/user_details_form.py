from wtforms import StringField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired

from librepos.forms.base import BaseForm

field_kw = {"placeholder": " "}

gender_choices = [("male", "Male"), ("female", "Female"), ("other", "Other")]
marital_status_choices = [
    ("single", "Single"),
    ("married", "Married"),
    ("divorced", "Divorced"),
    ("widowed", "Widowed"),
]


class UserDetailsForm(BaseForm):
    first_name = StringField(
        "First Name", validators=[DataRequired()], render_kw=field_kw
    )
    middle_name = StringField("Middle Name", render_kw=field_kw)
    last_name = StringField(
        "Last Name", validators=[DataRequired()], render_kw=field_kw
    )
    gender = SelectField("Gender", choices=gender_choices, default="male")
    marital_status = SelectField(
        "Marital Status", choices=marital_status_choices, default="single"
    )
    birthday = DateField("Birthday", render_kw=field_kw)
    submit = SubmitField("Update Details")
