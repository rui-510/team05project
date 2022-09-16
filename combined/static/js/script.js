$(function() {
    const socket = io();

    let id = $("#id").html();
    $('#roomid').val(id);

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

    // 名前の表示
    socket.on('display_name', function (msg) {
        let user = msg.name;
        $("#basic-addon3").html(user);
    });

    // メッセージが入力されると呼び出される
    $(".message").on("click", function (e) {
        id = $("#id").html();
        let text = $(this).text();
        let user_name = $("#basic-addon3").html();
        socket.emit("chat_message", { text: text , user: user_name , id: id });
    })

    // ショートカットキーの設定
    addEventListener( "keyup", (e) => {
        let key_code = e.key;
        const button = $(".message");
        if( key_code === "1") button[0].click();
        if( key_code === "2") button[1].click();
        if( key_code === "3") button[2].click();
        if( key_code === "4") button[3].click();
    });

    // メッセージの追加
    socket.on('chat_message', function (msg) {
        $("<li>", {
            text: msg.text
        }).prependTo('#messages');
    });

    //接続した人に現在の画面を共有
    // socket.on('restore_message', function (msg) {
    //     for (let i = 0; i < msg.chat.length; i++) {
    //         $("<li>", {
    //             text: msg.chat[i]
    //         }).appendTo('#messages');
    //     }

    //     // 名前の取得
    //     let user = msg.name;
    //     //メッセージの入力欄の横に名前を表示
    //     $("#basic-addon3").html(user);
    // });

});