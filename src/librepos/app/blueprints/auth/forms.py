"""WTForms for auth blueprint."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class AuthForm(FlaskForm):
    """Form for creating/editing auth."""

    # Add your form fields here
    # name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Submit")
