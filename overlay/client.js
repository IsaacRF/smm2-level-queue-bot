if( window.WebSocket ){
    //---------------------------------
    //  Variables
    //---------------------------------
    socket = null;
    var reconnectIntervalMs = 10000;
    var apiAvatarEndPoint = "https://decapi.me/twitch/avatar/";

    function Connect() {
        socket = new WebSocket(API_Socket);

        socket.onopen = function()
        {
            // Format your Authentication Information
            var auth = {
                author: "IsaacRF239",
                website: "https://isaacrf.com",
                api_key: API_Key,
                events: [
                    "EVENT_SMM2QS_LEVEL_UPDATE",
                ]
            }
            //Send your Data to the server
            socket.send(JSON.stringify(auth));
        };

        socket.onerror = function(error)
        {
            console.log("Error: " + error);
        }

        socket.onmessage = function (message)
        {
            var jsonObject = JSON.parse(message.data);

            if(jsonObject.event == "EVENT_SMM2QS_LEVEL_UPDATE")
            {
                updateUI(jsonObject.data);
            }
        }

        socket.onclose = function ()
        {
            //  Connection has been closed by you or the server
            console.log("Connection Closed!");
            setTimeout(Connect, reconnectIntervalMs);
        }
    }

    /**
     * Updates UI according to data received
     * @param {string} jsonData
     */
    function updateUI(jsonData) {
        //UI Update
        var data = JSON.parse(jsonData);
        if (data.currentLevelCode != "") {
            $("#current-level .user-name").text(data.currentLevelUser);
            $("#current-level .level-code").text(data.currentLevelCode);
            $("#current-level").removeClass('empty');
        } else {
            $("#current-level").addClass('empty');
        }

        if (data.nextLevelCode != "") {
            $("#next-level .user-name").text(data.nextLevelUser);
            $("#next-level .level-code").text(data.nextLevelCode);
            $("#next-level").removeClass('empty');
        } else {
            $("#next-level").addClass('empty');
        }

        if (data.currentLevelCode != "" && data.nextLevelCode == "") {
            $("#container").addClass('empty');
        } else {
            $("#container").removeClass('empty');
        }

        $("#wins").text(data.wins);
        $("#skips").text(data.skips);

        if (data.currentLevelUser != "") {
            $.get(apiAvatarEndPoint + data.currentLevelUser, function(response) {
                $( "#current-level .user-avatar" ).attr('src', response);
            });
        }

        if (data.nextLevelUser != "") {
            $.get(apiAvatarEndPoint + data.nextLevelUser, function(response) {
                $( "#next-level .user-avatar" ).attr('src', response);
            });
        }
    }

    function startPrompt() {
        var duration = ui.prompt.settings.duration * 1000;
        var frequency = ui.prompt.settings.frequency * 1000;
        setTimeout(function() {
            ui.prompt.toggle(true);
            setInterval(function() {
                ui.prompt.toggle(true);
            }, frequency + duration);
        }, frequency);
    }

    function togglePrompt(autoClose = false) {
        $(".prompt").toggleClass("visible");
        setTimeout(function() {
            $(".prompt").find(".message").toggleClass("prompt-marquee")
        }, 500);
        if (autoClose) {
            setTimeout(ui.prompt.toggle, ui.prompt.settings.duration * 1000);
        }
    }

    window.ui = {
        update: updateUI,
        prompt: {
            start: startPrompt,
            toggle: togglePrompt,
            settings: {
                enabled: false,
                frequency: 2,
                duration: 5
            }
        }
    };

    if (typeof testsEnabled === 'undefined' || testsEnabled == false) {
        Connect();
    } else {
        console.log('Tests enabled, socket connection omitted. Remove tests.js import from index to enter prod mode');
        $(function() {
            $(".main-wrapper").addClass("test");
        });
    }

    if (ui.prompt.settings.enabled) {
        ui.prompt.start();
    }
}