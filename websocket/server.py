from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_socketio import SocketIO, send, emit
from cs50 import SQL

import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# cors_allowed_originは本来適切に設定するべき
socketio = SocketIO(app, cors_allowed_origins='*')

# ユーザー数
user_count = 0
# メッセージ
chat = []

# チャット画面表示
@app.route('/')
def index():
    return render_template('index.html')

# ユーザーが新しく接続すると実行
@socketio.on('connect')
def connect(auth):
    global user_count, chat

    # ユーザー名をランダムに決定(本来はデータベースから取得)
    user_name = "ゲスト" + str(random.randint(0, 100))

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


# メッセージが送信されると実行
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