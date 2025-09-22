from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

from librepos.utils.form import default_placeholder, textarea_attributes
from librepos.common.forms import BaseForm


class RoleCreationForm(BaseForm):
    """Form for creating roles in the system"""

    name = StringField(
        "Name", validators=[DataRequired()], render_kw=default_placeholder
    )
    description = TextAreaField(
        "Description",
        validators=[DataRequired()],
        render_kw=textarea_attributes,
    )

    def __init__(self, *args, **kwargs):
        super(RoleCreationForm, self).__init__(*args, **kwargs)
