$(function() {

    const socket = io();

    let id = $("#id").html();
    $('#roomid').val(id);

    const audio1 = $('#btn_audio1')[0];
    const audio2 = $('#btn_audio2')[0];
    const audio3 = $('#btn_audio3')[0];
    const audio4 = $('#btn_audio4')[0];


    // 接続者数の更新
    socket.on('count_update', function (msg) {
        let user = msg.name;
        // 人数の更新
        $('#user_count').html(msg.user_count);

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
        $('#members').append('<li class="accordion-header list-group-item list-group-item-light" id="flush-headingOne"></li>')
        $("<button>", {
            type: "button",
            text: msg.members[0],
            class: "accordion-button collapsed list-group-item list-group-item-light",
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
                class: "accordion-body list-group-item list-group-item-light"
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
        socket.emit("chat_message", { text: text , user: user_name , id: id , type: "button"});
    })

     // メッセージが入力されると呼び出される
    $("#form").on("submit", function (e) {
        e.preventDefault();
        id = $("#id").html();
        let text = $("#basic-url").val();
        let user_name = $("#basic-addon3").html();
        if (text) {
            socket.emit("chat_message", { text: text , user: user_name , id: id , type: "message"});
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
        // ボタンかチャットの判別
        if (msg.type) {
            $("<li>", { class: "button-msg box" }).prependTo('#messages');
        }
        else {
            $("<li>", { class: "chat-msg box" }).prependTo('#messages');
        }
        // メッセージ表示
        $("<p>", {
            text: msg.text,
            class: "content"
        }).prependTo($(".box")[0]);

        // タイトル表示
        $("<span>", {
            text: "　" + msg.user + " ",
            class: "title"
        }).prependTo($(".box")[0]);

        // 時刻表示
        $("<span>", {
            text: msg.date,
            class: "date"
        }).appendTo($(".title")[0]);
        msg.date

        // アイコン表示
        $("<span>", { class: "icon" }).prependTo($(".title")[0]);

        if(msg.text == '質問があります'){
            //連続クリックに対応
            audio1.currentTime = 0;
            //クリックしたら音を再生
            audio1.play();
        }
        if(msg.text == '次は自分が話したいです'){
            //連続クリックに対応
            audio2.currentTime = 0;
            //クリックしたら音を再生
            audio2.play();
        }
        if(msg.text == 'その意見には賛成です'){
            //連続クリックに対応
            audio3.currentTime = 0;
            //クリックしたら音を再生
            audio3.play();
        }
        if(msg.text == 'その意見には反対です'){
            //連続クリックに対応
            audio4.currentTime = 0;
            //クリックしたら音を再生
            audio4.play();
        }
    });

    // 音のオンオフの切り替え
    $("#mute").on("click", () => {
        if (audio1.muted) {
            audio1.muted = false;
        } else {
            audio1.muted = true;
        }
        if (audio2.muted) {
            audio2.muted = false;
        } else {
            audio2.muted = true;
        }
        if (audio3.muted) {
            audio3.muted = false;
        } else {
            audio3.muted = true;
        }if (audio4.muted) {
            audio4.muted = false;
        } else {
            audio4.muted = true;
        }
    })

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