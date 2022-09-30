# combined_pre3 概要
    conbined に、LINE によるログイン機能・通知機能を追加したもの

# pip するもの
    line-bot-sdk

# データベース構造
CREATE TABLE users (
        id INTEGER PRIMARY KEY NOT NULL,
        username TEXT NOT NULL,
        hash TEXT,
        nickname TEXT,
        is_lien_account INT DEFAULT 0,
        is_sent_line INT DEFAULT 0,
        is_anonymous INT DEFAULT 0
);
CREATE TABLE users (
        id INTEGER PRIMARY KEY NOT NULL,
        username TEXT NOT NULL,
        hash TEXT,
        nickname TEXT,
        is_lien_account INT DEFAULT 0,
        is_sent_line INT DEFAULT 0,
        is_anonymous INT DEFAULT 0
);
CREATE TABLE members(
        room_id INT(6),
        user_id INT,
        user_name TEXT NOT NULL,
        foreign key (room_id) references chat_room(id),
        foreign key (user_id) references "users"(id)
);