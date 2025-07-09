from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired

from librepos.utils.form import default_placeholder, textarea_attributes


class RoleCreationForm(FlaskForm):
    """Form for creating roles in the system"""

    name = StringField(
        "Name", validators=[DataRequired()], render_kw=default_placeholder
    )
    description = TextAreaField(
        "Description",
        validators=[DataRequired()],
        render_kw=textarea_attributes,
    )
    active = BooleanField("Active", default=True)
    submit = SubmitField("Create Role")

    def __init__(self, *args, **kwargs):
        super(RoleCreationForm, self).__init__(*args, **kwargs)
