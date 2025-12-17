from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email


class UserLoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
