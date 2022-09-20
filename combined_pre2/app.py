
'''
sqlite3 chat.db
CREATE TABLE users(
                    id INTEGER,
                    username TEXT NOT NULL,
                    nickname TEXT,
                    hash TEXT,
                    line_id TEXT,
                    is_line_account INTEGER NOT NULL,
                    is_anonymous INTEGER NOT NULL,
                    is_nickname INTEGER NOT NULL,
                    PRIMARY KEY(id)
                );

drop table users;

'''


from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_socketio import SocketIO, send, emit
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

import random

# line_login
import hashlib
import urllib.request
import urllib.parse
import json
import base64
from pprint import pprint
import os

# debug
from datetime import datetime

# クライアント情報
# Channel ID
client_id = "1657463989"
# Channel Secret
client_secret = "8b1f642b3675401700ccdf61769c2d14"
# Callback URL
redirect_uri = 'https://as159-cga-code50-106875009-v6j69x4w5fx66j-5000.githubpreview.dev/callback'

# LINE エンドポイント
authorization_url = "https://access.line.me/oauth2/v2.1/authorize"
token_url = 'https://api.line.me/oauth2/v2.1/token'
user_info_url = 'https://api.line.me/v2/profile'

bot_id = '@334pnoyy'
prof_url = 'https://api.line.me/oauth2/v2.1/verify'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///chat.db")

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


@app.route("/line_redirect")
def line_redirect():

    # ステート生成
    state = hashlib.sha256(os.urandom(32)).hexdigest()
    session['state'] = state

    # 認可リクエスト
    return redirect(authorization_url+'?{}'.format(urllib.parse.urlencode({
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'state': state,
        'scope': "openid",
        'response_type': 'code',
        'bot_prompt': "aggressive",
        # 'prompt': "consent"
    })))


# ホーム画面表示
@app.route('/callback')
def callback():

     # 2. ユーザー認証/同意を行い、認可レスポンスを受け取る。
    # 認可コードを受け取る:https://developers.line.biz/ja/docs/line-login/integrate-line-login-v2/#receiving-the-authorization-code
    state = request.args.get('state')

    if state != session['state']:
        print("invalid_redirect")

    code = request.args.get('code')

    # 3. 認可レスポンスを使ってトークンリクエストを行う。 ステップごとに処理を確認、　ここまで実行できている、　具体的に
    # ウェブアプリでアクセストークンを取得する:https://developers.line.biz/ja/docs/line-login/integrate-line-login-v2/#get-access-token
    body = urllib.parse.urlencode({
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }).encode('utf-8')

    req_token, res_token = '', ''
    req_token = urllib.request.Request(token_url)

    try:
        with urllib.request.urlopen(req_token, data=body) as f:
            res_token = f.read()
    except Exception as e:
        print(e.read())

    access_token = json.loads(res_token)['access_token']

    # 4. 取得したアクセストークンを使用してユーザープロフィールを取得する。 ＞＞　LINE発行のユーザIDを、保存する　ユーザのデータベースも作る
    # ユーザープロフィールを取得する:https://developers.line.biz/ja/docs/line-login/managing-users/#get-profile
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    req_token = urllib.request.Request(user_info_url, headers=headers, method='GET')

    try:
        with urllib.request.urlopen(req_token) as f:
            res_token = f.read()
    except Exception as e:
        print(e.read())

    # 削除・登録し直し・引き継ぎしない以外、変更なし
    id_token = json.loads(res_token)['id_token']

### #########################

    # 3. 認可レスポンスを使ってトークンリクエストを行う。 ステップごとに処理を確認、　ここまで実行できている、　具体的に
    # ウェブアプリでアクセストークンを取得する:https://developers.line.biz/ja/docs/line-login/integrate-line-login-v2/#get-access-token
    body = urllib.parse.urlencode({
        'id_token': id_token,
        'client_id': client_id,
    }).encode('utf-8')

    req_prof, res_prof = '', ''
    req_token = urllib.request.Request(prof_url)

    try:
        with urllib.request.urlopen(req_prof, data=body) as f:
            res_prof = f.read()
    except Exception as e:
        print(e)

    print(res_prof)
    # access_token = json.loads(res_prof)['access_token']

    # 4. 取得したアクセストークンを使用してユーザープロフィールを取得する。 ＞＞　LINE発行のユーザIDを、保存する　ユーザのデータベースも作る
    # ユーザープロフィールを取得する:https://developers.line.biz/ja/docs/line-login/managing-users/#get-profile
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    req_prof = urllib.request.Request(user_info_url, headers=headers, method='GET')

    print(req_prof)
    print(res_prof)


    try:
        with urllib.request.urlopen(req_prof) as f:
            res_prof = f.read()
    except Exception as e:
        print(e.read())

    # return json.loads(res_token)
    # return json.loads(res_prof)

    id_token = generate_password_hash(id_token)

    # どちらでもいい情報
    access_token = generate_password_hash(access_token)

    # user情報をもらってくるときには、APIを叩く
    # チャットのルームが１つのlienのルームと結びつく。　チャットに参加した人はlineにも参加した事になっている。
    #　メッセージを送るときに、
    # id_token -> line_token

    try:
        new_user = db.execute("INSERT INTO users (username, nickname, is_line_account, is_anonymous, is_nickname) VALUES (?, 'nickname', 1, 0, 0)", id_token)
    except:
        return apology("Sorry.... Uh oh! Something went wrong!! ErrorCode: Line Login ")

    session["user_id"] = new_user

    return redirect("/")


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

        is_anonymous = request.form.get("sample1radio")
        is_nickname = request.form.get("sample2radio")
        print(is_nickname)
        new_nickname = request.form.get("nickname")

        is_nickname = 1

        if is_anonymous == "1":
            is_anonymous = 1 # 匿名on
        else:
            is_anonymous = 0 # 匿名off

        if is_nickname == "1":
            is_nickname = 1 # ニックネームon
        else:
            is_nickname = 0 # ニックネームoff

        old_nickname = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])#[2]["nickname"]

        if new_nickname != old_nickname: # 登録されているnicknameが変更された時には、データベース更新
            db.execute("UPDATE users SET nickname = ? WHERE id = ?", new_nickname, session["user_id"])

        db.execute("UPDATE users SET is_anonymous = ? WHERE id = ?", is_anonymous, session["user_id"]) # 匿名更新
        db.execute("UPDATE users SET is_nickname = ? WHERE id = ?", is_nickname, session["user_id"]) # ニックネーム更新

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

        # session["test"] = datetime.now()
        # print(session)

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
            new_user = db.execute("INSERT INTO users (username, hash, nickname, is_line_account, is_anonymous, is_nickname) VALUES (?, ?, 'nickname', 0, 0, 0)", username, hash)
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

    # usersのテーブルから、ユーザーの 匿名・ニックネーム 機能　on/off　を確認
    is_anonymous = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["is_anonymous"]
    is_nickname = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["is_nickname"]
    print(is_nickname)


    if is_anonymous == 0: # 匿名off
        if is_nickname == 1: # ニックネームoff
            # ユーザー名をデータベースから取得
            user_name = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["username"]
        else: # ニックネームon
            user_name = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["nickname"]
    else:
        user_name = "Anonymous" # 匿名on

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