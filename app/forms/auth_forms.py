from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=3,max=32)])
    email = EmailField('E-mail', validators=[DataRequired(), Email(), Length(min=3,max=320)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=5,max=64)])
    confirm_password = PasswordField('Confirme contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')