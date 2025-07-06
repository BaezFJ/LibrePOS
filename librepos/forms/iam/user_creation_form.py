from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email


class UserCreationForm(FlaskForm):
    role_id = SelectField(
        "Role", coerce=int, validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    username = StringField(
        "Username", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email()], render_kw={"placeholder": " "}
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    submit = SubmitField("Create User")

    def __init__(self, **kwargs):
        super(UserCreationForm, self).__init__(**kwargs)

        from librepos.repositories import RoleRepository

        active_roles = RoleRepository().get_active_roles()

        self.role_id.choices = [
            (r.id, r.name.replace("_", " ").title()) for r in active_roles
        ]
