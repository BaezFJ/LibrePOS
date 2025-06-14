from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email


class UserRegistrationForm(FlaskForm):
    role_id = SelectField(
        "Role", coerce=int, validators=[DataRequired()], render_kw={"placeholder": " "}
    )

    first_name = StringField(
        "First Name", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    middle_name = StringField("Middle Name", render_kw={"placeholder": " "})
    last_name = StringField(
        "Last Name", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email()], render_kw={"placeholder": " "}
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    gender = SelectField(
        "Gender",
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        validators=[DataRequired()],
        render_kw={"placeholder": " "},
    )
    submit = SubmitField("Register")

    def __init__(self, **kwargs):
        super(UserRegistrationForm, self).__init__(**kwargs)

        from librepos.models.roles import Role

        active_roles = Role.query.filter_by(active=True).all()
        self.role_id.choices = [(r.id, r.name.title()) for r in active_roles]
