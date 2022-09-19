＜＜連絡＞＞　
変更した箇所は、server.py, register.html, login.html, userのデータベース、の4点です。
”改修希望”でコードの中を検索して頂けると、レビューを希望するコードが分かりやすくなります。
LINEログインの箇所はあえて、動作する状態なので改修希望をしていませんが、よくなる箇所があればお願いします。

僕が作成した実装を動作するように追加していきましたが、コードの品質が悪く、読みにくい状態であると思います。
なので、もし平岡さんの時間があれば、申し訳ありませんが修正・確認等をよろしくお願い致します。
コードの意図や動きが分からないところがあれば、自分の認識をお伝えしますので、なんでも聞いて下さい。

以上、長くなりましたがよろしくお願い致します！！　

林


＜＜データベースについて＞＞
追加したカラムは以下の2つです。
    'nickname' TEXT,
    is_nickname INTEGER default 0,
    is_line_account INTEGER　default 0

LINEログインでのデータベース登録処理についてですが、特殊になっています。
まず、LINEのサーバで認証を行なっている為、hashは不要にしています。
さらに、subは新たに　line_id　のカラムも追加しようか迷いましたが、複雑さをなくすためusernameに登録しています。


元々の設計
CREATE TABLE IF NOT EXISTS 'users' (
        'id' INTEGER PRIMARY KEY NOT NULL,
        'username' TEXT NOT NULL,
        'hash' TEXT NOT NULL,
        is_anonymous INTEGER default 0,
    );
CREATE TABLE chat_room (
        id INT(6) PRIMARY KEY NOT NULL,
        password VARCHER(10)  NOT NULL,
        people_num INT default 0 not null
    );


