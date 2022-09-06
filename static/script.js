$(function() {
    const socket = io();

    // 接続者数の更新
    socket.on('count_update', function (msg) {
        let user = msg.name;
        $('#user_count').html(msg.user_count);
        // 入室通知
        if (msg.alert) {
            $("#enter").html(user);
            $(".alert").fadeIn();
            setTimeout(() => {
                $(".alert").fadeOut();
            }, 2000);
        }
    });

    // メッセージが入力されると呼び出される
    $("#form").on("submit", function (e) {
        let val = $("#basic-url").val();
        let user_name = $("#basic-addon3").html();
        e.preventDefault();
        //メッセージがある時のみサーバー側に送信する
        if (val) {
            socket.emit("chat_message", { message: val , user: user_name });
            $("#basic-url").val("");
        }
    })

    // メッセージの追加
    socket.on('chat_message', function (msg) {
        $("<li>", {
            text: msg.message
        }).appendTo('#messages');
    });

    //接続した人に現在の画面を共有
    socket.on('restore_message', function (msg) {
        for (let i = 0; i < msg.chat.length; i++) {
            $("<li>", {
                text: msg.chat[i]
            }).appendTo('#messages');
        }

        // 名前の取得
        let user = msg.name;
        //メッセージの入力欄の横に名前を表示
        $("#basic-addon3").html(user);
    });
});