$(function() {
    const socket = io();

    let id = $("#id").html();
    $('#roomid').val(id);

    const audio = $('#btn_audio')[0];

    // 接続者数の更新
    socket.on('count_update', function (msg) {
        let user = msg.name;
        // 人数の更新
        $('#user_count').html(msg.user_count);
        $('#good_count').html(msg.good_count);

        // 入室通知
        if (msg.alert) {
            $("#enter").html(user);
            $(".alert").fadeIn();
            setTimeout(() => {
                $(".alert").fadeOut();
            }, 2000);
        }

        // メンバーを全部削除
        let members = $("#members")[0];
        while(members.firstChild){
            members.removeChild(members.firstChild);
        }

        // 最初の人を表示
        $('#members').append('<li class="accordion-header list-group-item list-group-item-info" id="flush-headingOne"></li>')
        // $('#members').append('<button class="accordion-button collapsed list-group-item list-group-item-info" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne"><button>')
        $("<button>", {
            type: "button",
            text: msg.members[0],
            class: "accordion-button collapsed list-group-item list-group-item-info",
            "data-bs-toggle": "collapse",
            "data-bs-target": "#flush-collapseOne",
            "aria-expanded": "false",
            "aria-controls": "flush-collapseOne"
        }).appendTo('#flush-headingOne');

        // ルーム内のメンバーの更新
        $('#members').append('<div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#accordionFlushExample"></div>')
        for (let i = 1; i < msg.members.length; i++) {
            $("<li>", {
                text: msg.members[i],
                class: "accordion-body list-group-item list-group-item-info"
            }).appendTo('#flush-collapseOne');
        }
    });

    // 名前の表示
    socket.on('display_name', function (msg) {
        let user = msg.name;
        $("#basic-addon3").html(user);
    });

    // ボタンが押されると呼び出される
    $(".message").on("click", function (e) {
        id = $("#id").html();
        let text = $(this).text();
        let user_name = $("#basic-addon3").html();
        socket.emit("chat_message", { text: text , user: user_name , id: id });
    })

     // メッセージが入力されると呼び出される
    $("#form").on("submit", function (e) {
        e.preventDefault();
        id = $("#id").html();
        let text = $("#basic-url").val();
        let user_name = $("#basic-addon3").html();
        if (text) {
            socket.emit("chat_message", { text: text , user: user_name , id: id });
            $("#basic-url").val("")
        }
    })

    // ショートカットキーの設定
    addEventListener("keyup", (e) => {
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

        //連続クリックに対応
        audio.currentTime = 0;
        //クリックしたら音を再生
        audio.play();
    });

    // 音のオンオフの切り替え
    $("#mute").on("click", () => {
        if (audio.muted) {
            audio.muted = false;
        } else {
            audio.muted = true;
        }
    })

    // いいね！機能:現在没仕様だが、使えそう
    // $("#good").on("click", () => {
    //         good_count += good_count;
    // })

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