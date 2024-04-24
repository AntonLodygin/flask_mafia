from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class LobbyForm(FlaskForm):
    title = StringField("Название лобби", validators=[DataRequired()], default="lobby")
    open = BooleanField("Открытое", default=True)
    password = PasswordField("Пароль")
    submit = SubmitField("Создать")
