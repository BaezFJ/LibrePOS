from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email


kw = {"placeholder": " "}


class UserForm(FlaskForm):
    def __init__(self, **kwargs):
        super(UserForm, self).__init__(**kwargs)

        from .models import Role

        active_roles = Role.query.filter_by(is_active=True).all()
        self.role_id.choices = [(r.id, r.name.title()) for r in active_roles]

    role_id = SelectField("Role", coerce=int, render_kw=kw)
    first_name = StringField("First Name", validators=[DataRequired()], render_kw=kw)
    last_name = StringField("Last Name", validators=[DataRequired()], render_kw=kw)
    username = StringField("Username", validators=[DataRequired()], render_kw=kw)
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw=kw)
    phone = StringField("Phone", render_kw=kw)
    hourly_rate = FloatField("Hourly Rate", validators=[DataRequired()], render_kw=kw)
    submit = SubmitField("Submit")
