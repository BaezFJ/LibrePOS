from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

field_kwargs = {'placeholder': " "}


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw=field_kwargs)
    password = PasswordField('Password', validators=[DataRequired()], render_kw=field_kwargs)
    submit = SubmitField('Login')
    
    
class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], render_kw=field_kwargs)
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()], render_kw=field_kwargs)
    submit = SubmitField('Reset Password')
    

class ReauthenticateForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], render_kw=field_kwargs)
    submit = SubmitField('Reauthenticate')