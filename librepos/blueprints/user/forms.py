from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

field_kwargs = {"placeholder": " "}


class UserProfileForm(FlaskForm):
    first_name = StringField(
        "First Name", validators=[DataRequired()], render_kw=field_kwargs
    )
    middle_name = StringField("Middle Name", render_kw=field_kwargs)
    last_name = StringField(
        "Last Name", validators=[DataRequired()], render_kw=field_kwargs
    )
    phone_number = StringField("Phone Number", render_kw=field_kwargs)
    address = StringField("Address", render_kw=field_kwargs)
    city = StringField("City", render_kw=field_kwargs)
    state = StringField("State", render_kw=field_kwargs)
    zip_code = StringField("Zip Code", render_kw=field_kwargs)
    country = StringField("Country", render_kw=field_kwargs)
    submit = SubmitField("Update")
