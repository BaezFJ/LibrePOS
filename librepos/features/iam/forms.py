from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import DataRequired


class CreateUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], render_kw={"autofocus": True})
    email = EmailField("Email", validators=[DataRequired()])


class CreateGroupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], render_kw={"autofocus": True})
    description = StringField("Description")
