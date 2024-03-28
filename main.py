from flask import Flask, render_template

from data import db_session
from data.lobbies import Lobby
from data.users import User
from data.players import Player

app = Flask(__name__)
db_session.global_init("db/blogs.db")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    db_sess = db_session.create_session()
    # user = User(mafia_winrate=111)
    # lobby = Lobby()
    # player = Player(user_id=1)
    # lobby.players.append(player)
    # db_sess.add(user)
    # db_sess.add(lobby)
    # db_sess.add(player)
    # db_sess.merge(lobby)
    # db_sess.commit()
    # print(lobby.players[0].user)

    app.run(port=7777)
