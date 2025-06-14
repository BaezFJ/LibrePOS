from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired


class RoleForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    description = TextAreaField(
        "Description",
        validators=[DataRequired()],
        render_kw={"placeholder": " ", " class": "materialize-textarea"},
    )
    active = BooleanField("Active", default=True)

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
