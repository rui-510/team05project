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

    // ショートカットキー(現状、「1」～「4」の数字)を押したときに、特定のボタンがクリックされるようにする
    //なにかキーが離された(「keyup」)とき、keydownfuncという関数を呼び出す
    addEventListener( "keyup", keydownfunc );
    function keydownfunc( event ) {
        //押されたボタンに割り当てられた数値を、key_codeに代入
        // 「event.key」：入力された文字を取得。フルキーボードの5でもNumPadの5でもevent.keyで取得されるのは"5"。
        // 注意点:(「ロケール(システムやソフトウェアにおける言語や国・地域の設定)やシステムレベルキーマップ(コンピューターのキーボードにおける、キーの文字・記号・機能の個別の割り当て)の影響を受ける」&「Android Browseには非対応」らしいので、エラーや動作不良の恐れ)
        var key_code = event.key;
        // 「===」は厳密等価演算子。データ型と値の両方が等しいか判断。「==」でも動作するが、より条件を厳しくしてバグ回避。
        if( key_code === "1") document.getElementById('btn1').click();
        if( key_code === "2") document.getElementById('btn2').click();
        if( key_code === "3") document.getElementById('btn3').click();
        if( key_code === "4") document.getElementById('btn4').click();
    }

    // ボタンがクリックされると呼び出される
    $(".btn").on("click", function (e) {
        let text = $(this).text();
        let user_name = $("#basic-addon3").html();
        e.preventDefault();
        //メッセージがある時のみサーバー側に送信する
        socket.emit("chat_message", { text: text , user: user_name });
    })

    // メッセージの追加
    socket.on('chat_message', function (msg) {
        $("<li>", {
            text: msg.text
        // メッセージを先頭に置くようにして、チャット数が長くなった時にスクロールせずに済むようにした。          
        }).prependTo('#messages');
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
