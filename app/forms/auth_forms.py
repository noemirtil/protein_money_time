from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3,max=32)])
    email = EmailField('E-mail', validators=[DataRequired(), Email(), Length(min=3,max=320)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5,max=64)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
class LoginForm(FlaskForm):
    username_email = StringField('Username or e-mail address', validators=[DataRequired(), Length(min=3,max=320)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5,max=64)])
    submit = SubmitField('Login')