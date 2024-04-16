from flask import Flask, render_template, redirect, request, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_socketio import SocketIO, emit, send

from data import db_session
from data.lobbies import Lobby
from data.players import Player
from data.users import User
from forms.lobby_form import LobbyForm
from forms.login_form import LoginForm
from forms.register_form import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mafia_secret_key'
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/blogs.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/register", methods=["GET", "POST"])
def register():
    db_sess = db_session.create_session()
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(email=form.email.data)
        new_user.set_password(form.password.data)
        db_sess.add(new_user)
        db_sess.commit()
        return redirect("/login")
    return render_template("register.html", form=form, title="Регистрация")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    db_sess = db_session.create_session()
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if not user:
            form.email.errors.append("Пользователь не найден")
        elif not user.check_password(form.password.data):
            form.password.errors.append("Неверный пароль")
        else:
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=form, title="Вход")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    db_sess = db_session.create_session()
    lobbies = db_sess.query(Lobby).filter(Lobby.players).all()
    return render_template("index.html", lobbies=lobbies, title="Мафия")


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
    return render_template("add_lobby.html", form=form, title="Создание лобби")


@app.route("/check_lobby_password/", methods=["POST"])
def check_lobby_password():
    db_sess = db_session.create_session()
    return "ok" if db_sess.query(Lobby).filter(Lobby.id == request.json["lobby_id"]).first().check_password(
        request.json["password"]) else "wrong"


if __name__ == '__main__':
    # db_sess = db_session.create_session()
    # user = User(email="qwe")
    # lobby = Lobby(title="open")
    # lobby1 = Lobby(title="close", open=False)
    # lobby1.set_password("qweqwe")
    # player = Player(user_id=1, lobby_id=1)
    # lobby.players.append(player)
    # db_sess.add(user)
    # db_sess.add(lobby)
    # db_sess.add(player)
    # db_sess.add(lobby1)
    # db_sess.commit()

    socketio.run(app, allow_unsafe_werkzeug=True, port=1337)
