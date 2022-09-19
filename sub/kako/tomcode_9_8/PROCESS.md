# 自分の足跡(グループ開発)
プレビュー：［Ctrl］＋［K］→［V］

## 2022/9/4
## flask-WebSocketのライブラリの選択
https://qiita.com/nanakenashi/items/6497caf1c56c36f47be9

```
作者の信頼度もGitHubのスターも同程度で悩みましたが
アップデートの頻度が高い
すぐに動くサンプルが付属している
という点から、Flask-SocketIOを選択しました。
```

→Flask-SocketIOを使用すべき？？

Flask-SocketIO：
https://github.com/miguelgrinberg/Flask-SocketIO


## Flask-SocketIOを使ってみる

https://kivantium.hateblo.jp/entry/2021/10/18/110509

成功。<br>
エンターキーを押さなくても同期される→どうやってデータを記憶＆送信？？？<br>
次は、このコードの一行一行の意味を解明してみる。<br>
https://flask-socketio.readthedocs.io/en/latest/index.html<br>
絶対これは使う


## 2022/9/5
「index.html」にとりあえずボタンを実装しよう！！<br>
参考とするもの：homepage/botton.html

思ったこと：<br>
接続者数が一人多いときがあった<br>
cssが効かない<br>
ヘッダーが効いてない<br>