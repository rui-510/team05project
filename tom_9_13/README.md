# README
## 更新ベース
「hira_09_08」(最終更新：2022/9/11)

## 更新点(更新日：2022/9/13)
ショートカットキーを離した(押し続けるた時に連投にならないようにした)際、特定のボタンが押されるようにした。

## 変えたところ
### 「chatroom.html」(24～27行)
・各ボタンの「id」を追加
### 「script.js」(18～31行)
・ショートカットキーを押した際、特定のボタンが押されるようなコードを挿入。

## 参考URL
・【JavaScript】キー入力でキャラを動かしてみよう！　小学生からのプログラミング入門<br>
https://original-game.com/introduction-to-javascript-move-a-character-by-input/

・JavaScriptのキーボードイベント、キー判定にどれつかう？<br>
https://qiita.com/riversun/items/3ff4f5ecf5c21b0548a4



## 再更新点(更新日：2022/9/14)
チャットメッセージを先頭に置くようにして、チャット数が長くなった時にスクロールせずに済むようにした。

## 変えたところ
「script.js」の「メッセージの追加」(47行)
          「appendTo('#messages')」→「prependTo('#messages')」<br>
  (＊変えたのはこれだけ。メッセージは下に行くほど最新のものというイメージが「LINE」や「Discord」等で作られてしまっているので、できれば改善したい気もする。)
  
  ## 参考URL
  ・jQuery 要素を追加/子要素の先頭最後(append)<br>
  https://itsakura.com/jquery-prepend
