from flask import Flask, render_template, redirect, request
from flask_socketio import SocketIO

from data import db_session
from data.lobbies import Lobby
from data.players import Player
from data.users import User
from forms.lobby_form import LobbyForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mafia_secret_key'
socketio = SocketIO(app)
db_session.global_init("db/blogs.db")


@app.route("/")
def index():
    db_sess = db_session.create_session()
    lobbies = db_sess.query(Lobby).all()
    # if request.form.get("lobby_password") == :
    #     return redirect("/lobby")
    return render_template("index.html", lobbies=lobbies)


@app.route("/lobby/<int:id>")
def lobby(id):
    return {}


@app.route("/add_lobby", methods=["GET", "POST"])
def add_lobby():
    form = LobbyForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        new_lobby = Lobby(title=form.title.data, user_count=form.users_count.data, open=form.open.data)
        new_lobby.set_password(form.password.data)
        db_sess.add(new_lobby)
        db_sess.commit()
        return redirect(f"/lobby/{new_lobby.id}")
    return render_template("add_lobby.html", form=form)


if __name__ == '__main__':
    # db_sess = db_session.create_session()
    # user = User()
    # lobby = Lobby()
    # lobby1 = Lobby(open=False)
    # lobby1.set_password("qweqwe")
    # player = Player()
    # lobby.players.append(player)
    # db_sess.add(user)
    # db_sess.add(lobby)
    # db_sess.add(player)
    # db_sess.add(lobby1)
    # db_sess.merge(lobby)
    # db_sess.commit()

    socketio.run(app, allow_unsafe_werkzeug=True, port=1337)
