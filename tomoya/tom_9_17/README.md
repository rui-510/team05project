# README
## 更新ベース
「conbined」(最終更新：2022/9/17)

## 更新点(更新日：2022/9/13)
①パスワード忘れ防止機能の実装(単にパスワードも表示するようにしただけ。プライバシーの考慮はしてないので、改善の余地あり。)
②チャットごとのタイムスタンプ機能の実装

## 変えたところ
①(＊パスワードIDと同じような仕様にすればよいという考えで更新しましたが、不要な更新点もあるかもしれません。)
### 「server.py」(34行)
「password = 0」
### 「server.py」の@app.route(146行～)
「global room_id, password」(150行)
「return render_template('chatroom.html', room_id=room_id, password=password)」(186行)
### 「chatroom.html」(23～25行)
(＊ルームIDと同様に表示。デザインは他との兼ね合いがあるため考慮していない。)<br><br>

②
###「server.py」(10行目)
「import datetime, pytz」
### 「server.py」の@socketio.on('chat_message')(328行～)<br>

## 参考URL
①(なし)
②【Python】現在時刻を表示するには？ datetime モジュール
https://aiacademy.jp/media/?p=1870
