from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

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