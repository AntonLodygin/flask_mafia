import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase

player_to_lobby = sqlalchemy.Table(
    "player_to_lobby", SqlAlchemyBase.metadata,
    sqlalchemy.Column("player", sqlalchemy.Integer, sqlalchemy.ForeignKey("players.id")),
    sqlalchemy.Column("lobby", sqlalchemy.Integer, sqlalchemy.ForeignKey("lobbies.id")))


class Player(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'players'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    role = sqlalchemy.Column(sqlalchemy.String)
    life = sqlalchemy.Column(sqlalchemy.Boolean)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship("User")
