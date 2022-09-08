'''
@team/@team_share/0908_naoki/

'''

import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_socketio import SocketIO, send, emit

# apologyという関数
from helpers import apology, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# テンプレートの自動再読み込みの確認
app.config["TEMPLATES_AUTO_RELOAD"] = True

# ファイルシステムを使用するようにセッションを構成する (署名入りCookieの代用として)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# CS50 ライブラリで SQLite データベースを使用するように設定する。
db = SQL("sqlite:///chat.db")

# cors_allowed_originは本来適切に設定するべき
socketio = SocketIO(app, cors_allowed_origins='*')

# ユーザー数
user_count = 0
# メッセージ
chat = []


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# チャット画面表示
@app.route('/')
@login_required
def index():
    return render_template('/register.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # GET POST 戻り値が両方必要
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if not username or not password or not confirmation:
            return apology("Fill in the Boxes")

        sql = None
        sql = "SELECT id FROM users WHERE username = ?"
        sql1 = db.execute(sql, username)

        if len(sql1) == 1:
            return apology("Username is already in use")

        if password != confirmation:
            return apology("Wrong Password", code=400)

        else:
            password = generate_password_hash(password)
            sql = "INSERT INTO users(username, hash) VALUES (?, ?)"
            db.execute(sql, username, password)

            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            print(rows)
            session["user_id"] = rows[0]["id"]
            print(session)

            return redirect("/")
    else:
        return render_template('register.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



    #####　以下、平岡さん　#####


# ユーザーが新しく接続すると実行
@socketio.on('connect')
def connect(auth):
    global user_count, chat
    user_count += 1
    # 接続者数の更新（全員向け）
    emit('count_update', {'user_count': user_count}, broadcast=True)
    # # テキストエリアの更新(接続した人のみ)
    emit('restore_message', {'chat': chat})


# ユーザーの接続が切断すると実行
@socketio.on('disconnect')
def disconnect():
    global user_count
    user_count -= 1
    # 接続者数の更新（全員向け）
    emit('count_update', {'user_count': user_count}, broadcast=True)


# メッセージが送信されると実行
@socketio.on('chat_message')
def chat_message(json):
    global chat
    message = json["message"]
    chat.append(message)
    # メッセージを全員に送信
    emit('chat_message', {'message': message}, broadcast=True)


if __name__ == '__main__':
    # 本番環境ではeventletやgeventを使うらしいが簡単のためデフォルトの開発用サーバーを使う
    socketio.run(app, debug=True)



'''
・セッションの有効期限が長いかもしれない
・
'''