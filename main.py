from random import shuffle

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_restful import Api
from flask_socketio import SocketIO, emit

from data import db_session
from data.lobbies import Lobby
from data.players import Player
from data.user_api import UserResource, UsersListResource
from data.users import User
from forms.lobby_form import LobbyForm
from forms.login_form import LoginForm
from forms.register_form import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mafia_secret_key'
socketio = SocketIO(app)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/blogs.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.id == user_id).first()


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            form.login.errors.append("Пользователь с этой почтой уже существует")
        elif form.password.data != form.password_repeat.data:
            form.password_repeat.errors.append("Пароли не совпадают")
        elif not db_sess.query(User).filter(
                User.login == form.login.data).first() and form.password.data == form.password_repeat.data:
            new_user = User(login=form.login.data)
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
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if not user:
            form.login.errors.append("Пользователь не найден")
        elif not user.check_password(form.password.data):
            form.password.errors.append("Неверный пароль")
        else:
            login_user(user)
            return redirect("/lobby_list")
    return render_template("login.html", form=form, title="Вход")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/lobby_list")
@login_required
def lobby_list():
    db_sess = db_session.create_session()
    lobbies = [i for i in db_sess.query(Lobby).filter(Lobby.players).all() if len(i.players) < 10]
    return render_template("lobby_list.html", lobbies=list(lobbies), title="Мафия")


@app.route("/lobby/<int:id>")
@login_required
def lobby(id):
    db_sess = db_session.create_session()
    lobby = db_sess.query(Lobby).filter(Lobby.id == id).first()
    return render_template("lobby.html", players=lobby.players)


@app.route("/add_lobby", methods=["GET", "POST"])
@login_required
def add_lobby():
    form = LobbyForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        new_lobby = Lobby(title=form.title.data, open=form.open.data)
        new_lobby.set_password(form.password.data)
        player = Player(user_id=current_user.id, lobby_id=new_lobby.id)
        db_sess.add(new_lobby)
        db_sess.add(player)
        db_sess.commit()
        return redirect(f"/lobby/{new_lobby.id}")
    return render_template("add_lobby.html", form=form, title="Создание лобби")


@app.route("/check_lobby_password/", methods=["POST"])
def check_lobby_password():
    db_sess = db_session.create_session()
    return "ok" if db_sess.query(Lobby).filter(Lobby.id == request.json["lobby_id"]).first().check_password(
        request.json["password"]) else "wrong"


@socketio.on("user_join")
def user_join(data):
    db_sess = db_session.create_session()
    print("join", data, current_user.login)
    lobby = db_sess.query(Lobby).filter(Lobby.id == data["room"]).first()
    if db_sess.query(Player).filter(Lobby.user_id == current_user.id).first() not in lobby.players:
        lobby.players.append(Player(user_id=current_user.id, lobby_id=lobby.id))
        db_sess.merge(lobby)
    db_sess.commit()
    emit("player joined", {"user_login": current_user.login}, broadcast=True)
    if len(lobby.players) == 10:
        print("lobby full")
        emit("lobby full", broadcast=True)


@socketio.on("user_leave")
def user_leave(data):
    db_sess = db_session.create_session()
    print("leave", data)
    lobby = db_sess.query(Lobby).filter(Lobby.id == data["room"]).first()
    lobby.players.remove(Player(user_id=current_user.id, lobby_id=lobby.id))
    db_sess.merge(lobby)
    db_sess.commit()


@socketio.on("get roles")
def get_roles(data):
    db_sess = db_session.create_session()
    players = db_sess.query(Lobby).filter(Lobby.id == data["lobby_id"]).first().players
    if not all([p.role for p in players]):
        roles = ["mafia"] * 2 + ["don", "sheriff"] + ["civilian"] * 6
        shuffle(roles)
        for i, ii in enumerate(players):
            ii.role = roles[i]
            if ii.user == current_user:
                user_id = i
        db_sess.commit()
    else:
        for i, ii in enumerate(players):
            if ii.user == current_user:
                user_id = i
                break
    db_sess.commit()
    emit("get roles successful", {"players_roles": {str(j): jj.role for j, jj in enumerate(db_sess.query(Lobby).filter(
        Lobby.id == data["lobby_id"]).first().players)}, "user_id": user_id}, broadcast=True)


@socketio.on("start game")
def start_game(data):
    print("start game")
    db_sess = db_session.create_session()
    lobby = db_sess.query(Lobby).filter(Lobby.id == data["lobby_id"]).first()
    lobby.turn = "mafia"
    emit("game", {"turn": "mafia", "players_lifes": {str(j): jj.life for j, jj in lobby.players},
                  "players_roles": {str(j): jj.role for j, jj in lobby.players}}, broadcast=True)


@socketio.on("kill")
def kill(data):
    print("kill", data)
    db_sess = db_session.create_session()
    lobby = db_sess.query(Lobby).filter(Lobby.id == data["lobby_id"]).first()
    lobby.players[data["player_id"]].life = False
    lobby.turn = "don"
    db_sess.commit()
    players = db_sess.query(Lobby).filter(Lobby.id == data["lobby_id"]).first().players
    emit("game", {"turn": "don", "players_lifes": {str(j): jj.life for j, jj in players},
                  "players_roles": {str(j): jj.role for j, jj in players}}, broadcast=True)


@socketio.on("check on sheriff")
def check_on_sheriff(data):
    print("check on sheriff", data)
    db_sess = db_session.create_session()
    lobby = db_sess.query(Lobby).filter(Lobby.id == data["lobby_id"]).first()
    lobby.turn = "sheriff"
    db_sess.commit()
    emit("check on sheriff successful", {"player_id": data["player_id"],
                                         "is_sherif": lobby.players[data["player_id"]].role == "sheriff"})
    emit("game", {"turn": "sheriff", "players_lifes": {str(j): jj.life for j, jj in lobby.players},
                  "players_roles": {str(j): jj.role for j, jj in lobby.players}}, broadcast=True)


@socketio.on("check on mafia")
def check_on_mafia(data):
    print("check on mafia", data)
    db_sess = db_session.create_session()
    lobby = db_sess.query(Lobby).filter(Lobby.id == data["lobby_id"]).first()
    lobby.turn = "mafia"
    db_sess.commit()
    emit("check on mafia successful", {"player_id": data["player_id"],
                                       "is_mafia": lobby.players[data["player_id"]].role in ("mafia", "don")})
    emit("game", {"turn": "mafia", "players_lifes": {str(j): jj.life for j, jj in lobby.players},
                  "players_roles": {str(j): jj.role for j, jj in lobby.players}}, broadcast=True)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    db_sess = db_session.create_session()
    photo_name = None
    if request.method == "POST":
        photo_name = request.files["photo"].filename
        if photo_name:
            with open(f"static/images/{photo_name}", "wb+") as image:
                image.write(request.files["photo"].read())
            db_sess.query(User).filter(User.id == current_user.id).first().avatar = photo_name
            db_sess.commit()
    return render_template("profile.html", photo_name=photo_name, title="Профиль")


api.add_resource(UsersListResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')

if __name__ == '__main__':
    db_sess = db_session.create_session()
    user1 = User(login="q1")
    user1.set_password("q1")
    user2 = User(login="q2")
    user2.set_password("q2")
    lobby1 = Lobby(title="close", open=False)
    lobby1.set_password("qweqwe")
    lobby2 = Lobby(title="open", open=True)
    player1 = Player(user_id=1, lobby_id=1)
    player2 = Player(user_id=2, lobby_id=2)
    lobby1.players.append(player1)
    lobby2.players.append(player2)
    db_sess.add(user1)
    db_sess.add(user2)
    db_sess.add(lobby1)
    db_sess.add(lobby2)
    db_sess.add(player1)
    db_sess.add(player2)
    l = Lobby(open=False)
    l.set_password("qweqwe")
    db_sess.add(l)
    db_sess.commit()
    for i in range(8):
        u = User(login=f"i{i}")
        u.set_password(f"i{i}")
        db_sess.add(u)
        db_sess.commit()
        p = Player(user_id=u.id, lobby_id=l.id)
        db_sess.add(p)
        l.players.append(p)
        db_sess.merge(l)
        db_sess.commit()
    user_user = User(login="user", mafia_winrate=12, civilians_winrate=55, match_count=3255)
    user_user.set_password("user")
    user_user2 = User(login="user2")
    user_user2.set_password("user2")
    db_sess.add(user_user)
    db_sess.add(user_user2)
    db_sess.commit()
    socketio.run(app, port=1234, allow_unsafe_werkzeug=True)
