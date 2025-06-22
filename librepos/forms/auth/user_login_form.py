from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, StringField
from wtforms.validators import DataRequired


class UserLoginForm(FlaskForm):
    email = StringField(
        "Username", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    remember = BooleanField("Remember Me")
