import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

def password_check(form, field):
    msg = "Пароль должен содержать латинские сивмолы в верхнем и нижнем регистре и цифры"
    patern1 = re.compile('[a-z]+')
    patern2 = re.compile('[A-Z]+')
    patern3 = re.compile('\d+')
    if (not patern1.search(field.data) or
        not patern2.search(field.data) or
        not patern3.search(field.data)):
        raise ValidationError(msg)

class LoginForm(FlaskForm):
    mail = StringField("Имя:", validators=[DataRequired()])
    password = PasswordField("Пароль:", validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    mail = StringField(
        "Имя:", 
        validators=[
            DataRequired(),
            Length(min=4, max=32, message="Имя должно быть не менее 4 и не боле 32 символов"),
        ]
    )
    password = PasswordField(
        "Пароль:", 
        validators=[
            DataRequired(),
            Length(min=8, message="Пароль должен быть не менее 8 символов"),

            password_check
        ]
    )
    confirm_password = PasswordField("Пароль ещё раз:")

class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        "Пароль:", 
        validators=[
            DataRequired(),
            Length(min=8, message="Пароль должен быть не менее 8 символов"),
            EqualTo('confirm_password', message="Пароли не одинаковые"),
            password_check
        ]
    )
    confirm_password = PasswordField("Пароль ещё раз:")
