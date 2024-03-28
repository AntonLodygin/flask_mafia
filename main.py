from flask import Flask, render_template
from data.users import User
from data.lobbies import Lobby
from data import db_session

app = Flask(__name__)
db_session.global_init("db/blogs.db")



@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    db_sess = db_session.create_session()
    user = User()
    lobby = Lobby()
    lobby.users.append(user)
    db_sess.add(user)
    db_sess.add(lobby)
    db_sess.commit()
    print(lobby.users[0].id)
    app.run(port=7777)
