from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, StringField
from wtforms.validators import DataRequired


class AuthUserLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")


class AuthForgotPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
