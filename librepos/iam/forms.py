from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SubmitField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired


class UserLoginForm(FlaskForm):
    credentials = StringField("Email/Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
