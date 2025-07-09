from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Email

from librepos.utils.form import default_placeholder
from librepos.utils.formatters import un_snake_formatter

gender_choices = [("male", "Male"), ("female", "Female"), ("other", "Other")]
marital_status_choices = [
    ("single", "Single"),
    ("married", "Married"),
    ("divorced", "Divorced"),
    ("widowed", "Widowed"),
]


class UserCreationForm(FlaskForm):
    role_id = SelectField(
        "Role", coerce=int, validators=[DataRequired()], render_kw=default_placeholder
    )
    username = StringField(
        "Username", validators=[DataRequired()], render_kw=default_placeholder
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email()], render_kw=default_placeholder
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw=default_placeholder
    )
    submit = SubmitField("Create User")

    def __init__(self, **kwargs):
        super(UserCreationForm, self).__init__(**kwargs)

        from librepos.features.iam.repositories import RoleRepository

        active_roles = RoleRepository().get_active_roles()

        self.role_id.choices = [
            (r.id, un_snake_formatter(r.name).title()) for r in active_roles
        ]


class UserContactForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email()], render_kw=default_placeholder
    )
    phone = StringField("Phone", render_kw=default_placeholder)
    submit = SubmitField("Update Contact")


class UserAddressForm(FlaskForm):
    address = StringField(
        "Address", validators=[DataRequired()], render_kw=default_placeholder
    )
    city = StringField(
        "City", validators=[DataRequired()], render_kw=default_placeholder
    )
    state = StringField(
        "State", validators=[DataRequired()], render_kw=default_placeholder
    )
    zipcode = StringField(
        "Zipcode", validators=[DataRequired()], render_kw=default_placeholder
    )
    country = StringField(
        "Country", validators=[DataRequired()], render_kw=default_placeholder
    )
    submit = SubmitField("Update Address")


class UserDetailsForm(FlaskForm):
    first_name = StringField(
        "First Name", validators=[DataRequired()], render_kw=default_placeholder
    )
    middle_name = StringField("Middle Name", render_kw=default_placeholder)
    last_name = StringField(
        "Last Name", validators=[DataRequired()], render_kw=default_placeholder
    )
    gender = SelectField("Gender", choices=gender_choices, default="male")
    marital_status = SelectField(
        "Marital Status", choices=marital_status_choices, default="single"
    )
    birthday = DateField("Birthday", render_kw=default_placeholder)
    submit = SubmitField("Update Details")


class UserRoleForm(FlaskForm):
    role_id = SelectField(
        "Role",
        coerce=int,
        validators=[DataRequired()],
        render_kw=default_placeholder,
    )

    def __init__(self, **kwargs):
        super(UserRoleForm, self).__init__(**kwargs)

        from librepos.features.iam.repositories import RoleRepository

        self.role_id.choices = [
            (role.id, un_snake_formatter(role.name).title())
            for role in RoleRepository().get_active_roles()
        ]
