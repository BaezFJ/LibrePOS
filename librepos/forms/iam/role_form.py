from wtforms import TextAreaField
from wtforms.validators import DataRequired

from librepos.forms.base import NamedEntityForm


class RoleForm(NamedEntityForm):
    description = TextAreaField(
        "Description",
        validators=[DataRequired()],
        render_kw={"placeholder": " ", " class": "materialize-textarea"},
    )

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
