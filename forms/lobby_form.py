from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class LobbyForm(FlaskForm):
    title = StringField("Название лобби", validators=[DataRequired()], default="lobby")
    users_count = IntegerField("Количество игроков", validators=[DataRequired()], default=10)
    open = BooleanField("Открытое", default=True)
    password = PasswordField("Пароль")
    submit = SubmitField("Создать")
