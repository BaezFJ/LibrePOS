from flask_wtf import FlaskForm
from wtforms import BooleanField, FileField, PasswordField, SelectField, SubmitField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, ValidationError

from .models import IAMRole, IAMUser, UserGender, UserStatus


class UserLoginForm(FlaskForm):
    credentials = StringField("Email/Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class UserResetPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Reset Password")


class UserChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[DataRequired()])
    new_password = PasswordField(
        "New Password", validators=[DataRequired(), EqualTo("confirm_password")]
    )
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Update Password")


class UserRegisterForm(FlaskForm):
    role_id = SelectField("Role", coerce=int, validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    first_name = StringField("First Name", validators=[DataRequired()])
    middle_name = StringField("Middle Name", validators=[Optional()])
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


class UserEditForm(FlaskForm):
    image = FileField("Profile Image", validators=[Optional()])
    role_id = SelectField("Role", coerce=int, validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    first_name = StringField("First Name", validators=[DataRequired()])
    middle_name = StringField("Middle Name", validators=[Optional()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    status = SelectField("Status", validators=[DataRequired()])
    gender = SelectField(
        "Gender",
        choices=[(gender.value, gender.value.replace("_", " ").title()) for gender in UserGender],
        validators=[Optional()],
    )
    submit = SubmitField("Save Changes")

    def __init__(self, user=None, current_user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        # Populate status choices from UserStatus enum
        self.status.choices = [
            (status.value, status.value.replace("_", " ").title()) for status in UserStatus
        ]

        # Get all staff roles
        all_roles = IAMRole.get_all_staff_roles()

        # Filter roles based on the current user's role
        if current_user and current_user.role:
            current_role_name = current_user.role.name.lower()

            if current_role_name == "owner":
                filtered_roles = all_roles
            elif current_role_name == "admin":
                filtered_roles = [role for role in all_roles if role.name.lower() != "owner"]
            else:
                filtered_roles = [
                    role for role in all_roles if role.name.lower() not in ["owner", "admin"]
                ]
        else:
            filtered_roles = all_roles

        self.role_id.choices = [
            (role.id, str(role.name).replace("_", " ").title()) for role in filtered_roles
        ]

    def validate_username(self, field):
        user = IAMUser.get_first_by(username=field.data)
        if user and self.user and user.id != self.user.id:
            raise ValidationError("That username is already taken. Please choose another one.")

    def validate_email(self, field):
        user = IAMUser.get_first_by(email=field.data)
        if user and self.user and user.id != self.user.id:
            raise ValidationError("That email is already in use. Please choose another one.")
