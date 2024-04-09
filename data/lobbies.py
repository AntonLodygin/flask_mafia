import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Lobby(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'lobbies'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, default="Lobby")
    user_count = sqlalchemy.Column(sqlalchemy.Integer, default=10)
    open = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    players = orm.relationship("Player", secondary="player_to_lobby", backref="lobby")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
