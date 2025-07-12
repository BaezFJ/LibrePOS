from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, BooleanField, StringField
from wtforms.validators import DataRequired

from librepos.utils.form import default_placeholder, textarea_attributes


class MenuCategoryForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired()], render_kw=default_placeholder
    )
    description = TextAreaField("Description", render_kw=textarea_attributes)
    active = BooleanField("Active", default=True)
    submit = SubmitField("Add Category")

    def __init__(self, *args, submit_text=None, **kwargs):
        super().__init__(*args, **kwargs)
        if submit_text:
            self.submit.label.text = submit_text
