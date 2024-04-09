from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length


class CheckLobbyPasswordForm(FlaskForm):
    hidden_id = StringField()
    password = PasswordField()
    submit = SubmitField("OK")
