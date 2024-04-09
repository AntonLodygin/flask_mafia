from flask import Flask, render_template, redirect, request, url_for
from flask_socketio import SocketIO

from data import db_session
from data.lobbies import Lobby
from data.players import Player
from data.users import User
from forms.qwe_form import CheckLobbyPasswordForm
from forms.lobby_form import LobbyForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mafia_secret_key'
socketio = SocketIO(app)
db_session.global_init("db/blogs.db")


@app.route("/", methods=["GET", "POST"])
def index():
    # if request.method == "POST":
    #     print(request.form, request.form.get("lobby_id"))
    #     return redirect(url_for('lobby', id=request.form.get("lobby_id")))
    db_sess = db_session.create_session()
    lobbies = db_sess.query(Lobby).all()
    # # if request.form.get("lobby_password") == :
    # #     return redirect("/lobby")
    # ...
    # # redirect("/")
    forms = []
    for i in range(len(lobbies)):
        form = CheckLobbyPasswordForm()
        form.hidden_id.data = lobbies[i].id
        forms.append(form)
    if request.method == "POST":
        for form in forms:
            if form.validate_on_submit():
                print(form.hidden_id.data)


    return render_template("indexv2.html", lobbies=lobbies, forms=forms)


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


@app.route("/check_lobby_password")
def check_lobby_password():



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

    socketio.run(app, allow_unsafe_werkzeug=True, port=1212)
