if( window.WebSocket ){
    //---------------------------------
    //  Variables
    //---------------------------------
    socket = null;
    var reconnectIntervalMs = 10000;

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
                //SAMPLE
                var data = JSON.parse(jsonObject.data);
                $("#current-level .userName").text(data.currentLevelUser);
                $("#current-level .levelCode").text(data.currentLevelCode);
                $("#next-level .userName").text(data.nextLevelUser);
                $("#next-level .levelCode").text(data.nextLevelCode);
                $("#wins").text(data.wins);
                $("#skips").text(data.skips);
            }
        }

        socket.onclose = function ()
        {
            //  Connection has been closed by you or the server
            console.log("Connection Closed!");
            setTimeout(Connect, reconnectIntervalMs);
        }
    }

    Connect();
}