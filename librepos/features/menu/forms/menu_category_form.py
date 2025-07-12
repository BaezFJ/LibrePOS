from wtforms import TextAreaField, BooleanField, StringField
from wtforms.validators import DataRequired

from librepos.common.forms import BaseForm
from librepos.utils.form import default_placeholder, textarea_attributes


class MenuCategoryForm(BaseForm):
    name = StringField(
        "Name", validators=[DataRequired()], render_kw=default_placeholder
    )
    description = TextAreaField("Description", render_kw=textarea_attributes)
    active = BooleanField("Active", default=True)
