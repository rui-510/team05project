from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_socketio import SocketIO, send, emit
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# cors_allowed_originは本来適切に設定するべき
socketio = SocketIO(app, cors_allowed_origins='*')

# ユーザー数
user_count = 0
# メッセージ
chat = []

# ホーム画面表示
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# ルーム作成画面
@app.route('/make', methods=["GET", "POST"])
@login_required
def make():
    return render_template('make.html')

# ルーム参加処理
@app.route('/join', methods=["GET", "POST"])
@login_required
def join():
    if request.method == "POST":
        return render_template("chatroom.html")

    else:
        return render_template('join.html')

# チャット画面表示
@app.route('/chatroom', methods=["GET", "POST"])
@login_required
def chatroom():
    return render_template('chatroom.html')


""""""""""""""""""""""ログイン関連処理"""""""""""""""""""""""

# 新規登録の処理
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("You should fill username column")
        if not password:
            return apology("You should fill password column")
        if not confirmation:
            return apology("You should fill confirmation column")

        # ユーザとパスワードが一致していた場合、エラーを表示させる
        if username == password:
            return apology("username and password match!")

        # パスワードと再確認パスワードが一致していない場合、エラーを表示
        if password != confirmation:
            return apology("password and confirmation do not match!")

        # ユーザのパスワードの長さを3文字以上にする。
        if len(password) < 3:
            return apology("You should make your password more long")

        # パスワードがすべて１０進数の数字の場合、エラーを表示
        if password.isdecimal == True:
            return apology("please put non-numeric in password")

        # パスワードがすべて英字の場合、エラーを表示
        if password.isalpha == True:
            return apology("please put Non-English in password")

        hash = generate_password_hash(password)

        try:
            # 「""」も必要！
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("You already have registred username")

        session["user_id"] = new_user

        return redirect("/")

# ログイン処理
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            # エラー403とは、Webサイトが閲覧禁止となっている状態を表す
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

# ログアウト処理
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


"""""""""""""""""""""ユーザー接続処理"""""""""""""""""""""

# ユーザーが新しく接続すると実行
@socketio.on('connect')
def connect(auth):
    global user_count, chat

    # ユーザー名をデータベースから取得
    user_name = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["username"]

    # ユーザーの数を１増やす
    user_count += 1

    # 接続者数の更新（全員向けに送信）
    emit('count_update', {'user_count': user_count, 'name': user_name, 'alert': True}, broadcast=True)

    # テキストエリアの更新と名前の表示(接続した人のみに送信)
    emit('restore_message', {'chat': chat, 'name': user_name})


# ユーザーの接続が切断すると実行
@socketio.on('disconnect')
def disconnect():
    global user_count
    user_count -= 1
    # 接続者数の更新（全員向け）
    # 退室通知はしないようにする(alert = false)
    emit('count_update', {'user_count': user_count, 'alert': False}, broadcast=True)


# ボタンが押されるとメッセージを送信
@socketio.on('chat_message')
def chat_message(json):
    global chat
    text = json["text"]
    user = json["user"]
    user_text = user + " : " + text
    chat.append(user_text)
    print(text)
    # メッセージを全員に送信
    emit('chat_message', {'text': user_text}, broadcast=True)


if __name__ == '__main__':
    # 本番環境ではeventletやgeventを使うらしいが簡単のためデフォルトの開発用サーバーを使う
    socketio.run(app, debug=True)