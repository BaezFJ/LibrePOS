from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Email

field_kwargs = {"placeholder": " "}


class UserProfileForm(FlaskForm):
    first_name = StringField(
        "First Name", validators=[DataRequired()], render_kw=field_kwargs
    )
    middle_name = StringField("Middle Name", render_kw=field_kwargs)
    last_name = StringField(
        "Last Name", validators=[DataRequired()], render_kw=field_kwargs
    )
    gender = SelectField("Gender", choices=[("male", "Male"), ("female", "Female")])
    birthday = DateField("Birthday", format="%Y-%m-%d", render_kw=field_kwargs)
    marital_status = SelectField(
        "Marital Status",
        choices=[
            ("single", "Single"),
            ("married", "Married"),
            ("divorced", "Divorced"),
            ("widowed", "Widowed"),
        ],
    )
    phone_number = StringField("Phone Number", render_kw=field_kwargs)
    email = StringField(
        "Email", validators=[DataRequired(), Email()], render_kw=field_kwargs
    )
    address = StringField("Address", render_kw=field_kwargs)
    city = StringField("City", render_kw=field_kwargs)
    state = StringField("State", render_kw=field_kwargs)
    zip_code = StringField("Zip Code", render_kw=field_kwargs)
    country = StringField("Country", render_kw=field_kwargs)
    submit = SubmitField("Update")
