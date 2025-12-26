from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, SubmitField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Email, ValidationError

from .models import IAMRole, IAMUser


class UserLoginForm(FlaskForm):
    credentials = StringField("Email/Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class UserRegisterForm(FlaskForm):
    role_id = SelectField("Role", coerce=int, validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    submit = SubmitField("Register")

    def __init__(self, current_user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get all staff roles
        all_roles = IAMRole.get_all_staff_roles()

        # Filter roles based on the current user's role
        if current_user and current_user.role:
            current_role_name = current_user.role.name.lower()

            # Owner can see all roles
            if current_role_name == "owner":
                filtered_roles = all_roles
            # Admin cannot see an owner role
            elif current_role_name == "admin":
                filtered_roles = [role for role in all_roles if role.name.lower() != "owner"]
            # Other roles cannot see owner or admin roles
            else:
                filtered_roles = [
                    role for role in all_roles if role.name.lower() not in ["owner", "admin"]
                ]
        else:
            # No current user, show all roles
            filtered_roles = all_roles

        self.role_id.choices = [
            (role.id, str(role.name).replace("_", " ").title()) for role in filtered_roles
        ]

    def validate_username(self, field):
        user = IAMUser.get_first_by(username=field.data)
        if user:
            raise ValidationError("That username is already taken. Please choose another one.")

    def validate_email(self, field):
        email = IAMUser.get_first_by(email=field.data)
        if email:
            raise ValidationError("That email is already in use. Please choose another one.")
