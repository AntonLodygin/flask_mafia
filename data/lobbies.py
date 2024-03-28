import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Lobby(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'lobbies'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    user_count = sqlalchemy.Column(sqlalchemy.Integer)
    type = sqlalchemy.Column(sqlalchemy.Boolean)
    users = orm.relationship("User", secondary="user_to_lobby", backref="lobby")
