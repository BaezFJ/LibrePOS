from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, EmailField, SubmitField, SelectField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Email, EqualTo

from librepos.auth import models as auth_models


class UserLoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class UserRegisterForm(FlaskForm):
    role_id = SelectField("Role", coerce=int)
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"class": "validate", "placeholder": " "},
    )
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    first_name = StringField("First Name", validators=[DataRequired()])
    middle_name = StringField("Middle Name")
    last_name = StringField("Last Name", validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.role_id.choices = [
            (role.id, str(role.name).replace("_", " ").title())
            for role in auth_models.AuthRole.get_all()
        ]
