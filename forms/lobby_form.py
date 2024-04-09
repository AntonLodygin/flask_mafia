from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length


class LobbyForm(FlaskForm):
    title = StringField("Название лобби", validators=[DataRequired()], default="lobby")
    users_count = IntegerField("Количество игроков", validators=[DataRequired()], default=10)
    open = BooleanField("Открытое", default=True)
    password = PasswordField("Пароль", validators=[Length(min=4)])
    submit = SubmitField("Создать")