from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email()], render_kw={"placeholder": " "}
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    remember = BooleanField("Remember Me")
