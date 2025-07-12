from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Length


class BaseForm(FlaskForm):
    submit = SubmitField("Submit")

    def __init__(self, *args, submit_text=None, **kwargs):
        super().__init__(*args, **kwargs)
        if submit_text:
            self.submit.label.text = submit_text

        # Move the submit field to the end
        if 'submit' in self._fields:
            submit_field = self._fields.pop('submit')
            self._fields['submit'] = submit_field


class ConfirmationForm(FlaskForm):
    confirmation = StringField("Confirmation", validators=[DataRequired(), Length(min=6, max=15)])
    submit = SubmitField("Confirm")
