from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, HiddenField
from wtforms.validators import DataRequired


class ConfirmDeletionForm(FlaskForm):
    id = HiddenField("ID", validators=[DataRequired()])
    confirmation = StringField("Type 'confirm' to delete", validators=[DataRequired()])
    submit = SubmitField("Confirm Deletion", render_kw={"class": "btn danger"})