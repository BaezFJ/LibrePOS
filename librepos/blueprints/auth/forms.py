from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    SubmitField,
    PasswordField,
)
from wtforms.validators import DataRequired, Email

kw = {"placeholder": " "}


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw=kw)
    password = PasswordField("Password", validators=[DataRequired()], render_kw=kw)
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
