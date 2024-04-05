from flask import Flask, render_template

from data import db_session
from data.lobbies import Lobby
from data.players import Player
from data.users import User
from forms.lobby_form import LobbyForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mafia_secret_key'
db_session.global_init("db/blogs.db")


@app.route("/")
def index():
    db_sess = db_session.create_session()
    lobbies = db_sess.query(Lobby).all()
    return render_template("index.html", lobbies=lobbies)


@app.route("/lobby/<int:id>")
def lobby(id):
    return {}

@app.route("/add_lobby")
def add_lobby():
    form = LobbyForm()
    return render_template("add_lobby.html", form=form)


if __name__ == '__main__':
    db_sess = db_session.create_session()
    user = User()
    lobby = Lobby()
    lobby1 = Lobby(open=False)
    player = Player()
    lobby.players.append(player)
    db_sess.add(user)
    db_sess.add(lobby)
    db_sess.add(player)
    db_sess.add(lobby1)
    db_sess.merge(lobby)
    db_sess.commit()

    app.run(port=7777)
