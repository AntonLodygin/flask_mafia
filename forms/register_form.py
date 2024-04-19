from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = EmailField('Логин', validators=[DataRequired("Это поле должно быть заполненно")])
    password = PasswordField('Пароль', validators=[DataRequired("Это поле должно быть заполненно")])
    password_repeat = PasswordField('Пароль ещё раз', validators=[DataRequired("Это поле должно быть заполненно")])
    submit = SubmitField('Зарегистрироваться')
