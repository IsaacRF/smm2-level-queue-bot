$(function() {
    if( !window.WebSocket ) {
        return;
    }

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
                ui.update(jsonObject.data);
            }
        }

        socket.onclose = function ()
        {
            //  Connection has been closed by you or the server
            console.log("Connection Closed!");
            setTimeout(Connect, reconnectIntervalMs);
        }
    }

    function Level(cardId) {
        var level = this;
        this.id = cardId;
        this.card = $(`#${cardId}`);
        this.user = this.card.find(".user-name");
        this.code = this.card.find(".level-code");
        this.avatar = this.card.find(".user-avatar");
        this.avatarContainer = this.avatar.parent();
        this.visible = !this.card.is(".empty");

        this.update = function(data) {
            this.user.text(data.user);
            this.code.text(data.code);
            if (data.user in ui.avatarCache) {
                this.avatar.attr("src", ui.avatarCache[data.user]);
            } else {
                this.avatarContainer.addClass("loading");
                $.get(apiAvatarEndPoint + data.user, function(response) {
                    ui.avatarCache[data.user] = response;
                    level.avatar.attr("src", response);
                    level.avatarContainer.removeClass("loading");
                });
            }
        }

        this.hide = function() {
            this.card.addClass("empty");
            this.visible = false;
        }

        this.show = function() {
            this.card.removeClass("empty");
            this.visible = true;
        }

        this.toggle = function() {
            this.card.toggleClass("empty");
            this.visible = !this.visible;
        }

        this._playAnimation = function(animation, duration = 750, callback = null) {
            if (typeof duration === "undefined" || duration === null) {
                duration = 750;
            }
            this.card.addClass(animation);
            setTimeout(function() {
                level.card.removeClass(animation);
                if (callback != null && callback instanceof Function) {
                    callback();
                }
            }, duration);
        }

        this.slideIn = function(callback, forceDuration = null) {
            var animClass = `${this.id}-slide-in`;
            this.show();
            this._playAnimation(animClass, forceDuration, callback);
        }

        this.slideOut = function(callback, forceDuration = null) {
            var animClass = `${this.id}-slide-out`;
            this._playAnimation(animClass, forceDuration, callback);
        }

        if (this.id == "next-level") {
            this.moveToCurrent = function(callback, forceDuration = null) {
                this._playAnimation("next-level-to-current", forceDuration, callback);
            }
        }
    }

    var currentLevel = new Level('current-level');
    var nextLevel = new Level('next-level');

    /**
     * Updates UI according to data received
     * @param {string} jsonData
     */
    function updateUI(jsonData) {
        var data = JSON.parse(jsonData);
        var hasCurrent = (data.currentLevelCode != "");
        var hasNext = data.nextLevelCode != "";
        var currentLevelData = {
            user: data.currentLevelUser,
            code: data.currentLevelCode
        };
        var nextLevelData = {
            user: data.nextLevelUser,
            code: data.nextLevelCode
        };

        if (hasCurrent) {
            if (!currentLevel.visible) {
                currentLevel.update(currentLevelData);
                currentLevel.slideIn();
                if (hasNext) {
                    nextLevel.update(nextLevelData);
                    nextLevel.slideIn();
                }
            } else {
                if (currentLevelData.code != currentLevel.code.text()) {
                    currentLevel.slideOut(function() {
                        currentLevel.update(currentLevelData);
                    }, 1000);
                    nextLevel.moveToCurrent(function() {
                        if (hasNext) {
                            nextLevel.update(nextLevelData);
                            nextLevel.slideIn();
                        } else {
                            nextLevel.hide();
                        }
                    }, 1000);
                } else if (nextLevelData.code != nextLevel.code.text()) {
                    nextLevel.update(nextLevelData);
                    nextLevel.slideIn();
                }
            }
        } else {
            currentLevel.slideOut(function() {
                currentLevel.hide();
            });
        }

        if (!currentLevel.visible && !nextLevel.visible) {
            $("#container").addClass('empty');
        } else {
            $("#container").removeClass('empty');
        }

        $("#wins").text(data.wins);
        $("#skips").text(data.skips);
    }

    // Expose necessary functionalities
    window.ui = {
        update: updateUI,
        avatarCache: {},
        prompt: {
            start: function() {
                var duration = ui.prompt.settings.duration * 1000;
                var frequency = ui.prompt.settings.frequency * 1000;
                setTimeout(function() {
                    ui.prompt.toggle(true);
                    setInterval(function() {
                        ui.prompt.toggle(true);
                    }, frequency + duration);
                }, frequency);
            },
            toggle: function(autoClose = false) {
                $(".prompt").toggleClass("visible");
                setTimeout(function() {
                    $(".prompt").find(".message").toggleClass("prompt-marquee");
                }, 500);
                if (autoClose) {
                    setTimeout(ui.prompt.toggle, ui.prompt.settings.duration * 1000);
                }
            },
            settings: {
                enabled: true,
                frequency: 60,  // Show every X seconds
                duration: 20    // Show for X seconds (ideally, same as the marquee animation duration)
            }
        }
    };

    if (typeof testsEnabled === 'undefined' || testsEnabled == false) {
        Connect();
    } else {
        console.log('Tests enabled, socket connection omitted. Remove tests.js import from index to enter prod mode');
        $(".main-wrapper").addClass("test");
    }

    if (ui.prompt.settings.enabled) {
        ui.prompt.start();
    }

});