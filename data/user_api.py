from flask import jsonify, abort
from flask_restful import Resource, reqparse

from . import db_session
from .users import User

parser = reqparse.RequestParser()
parser.add_argument('login', required=True, type=str)
parser.add_argument('password', required=True, type=str)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, f"user {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({"user": user.to_dict(
            only=('mafia_winrate', 'civilians_winrate', 'match_count'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        args = parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        password = args["password"]
        if user.check_password(password):
            session.delete(user)
            session.commit()
            return jsonify({'message': 'user deleted'})
        else:
            return jsonify({'message': 'error password'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({"users": [user.to_dict(
            only=('mafia_winrate', 'civilians_winrate', 'match_count')) for user in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if not session.query(User).filter(User.login == args["login"]).first():
            user = User(
                login=args["login"]
            )
            user.set_password(args["password"])
            session.add(user)
            session.commit()
            return jsonify({"message": "user created", 'id': user.id})
        return jsonify({"message": "user already exists"})
