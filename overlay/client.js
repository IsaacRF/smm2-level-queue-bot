/*! SMM2 Level Queue System v1.1.0 | https://github.com/IsaacRF/smm2lqs | (c) IsaacRF239 & Gabriel Rodríguez | License GNU GPLv3
    Isaac Rodríguez Fernández | https://isaacrf.com
    Gabriel Rodríguez Fernández | https://twitter.com/Gabri239
*/

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
                author: "IsaacRF239 & Gabriel Rodríguez",
                website: "https://github.com/IsaacRF/smm2lqs",
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

    function UIElement(elementId) {
        this.id = elementId;
        this.element = $(`#${elementId}`);
        this.visible = !this.element.is(".hidden");
    }

    UIElement.prototype.hide = function() {
        this.element.addClass("hidden");
        this.visible = false;
    }

    UIElement.prototype.show = function() {
        this.element.removeClass("hidden");
        this.visible = true;
    }

    UIElement.prototype.toggle = function() {
        this.element.toggleClass("hidden");
        this.visible = !this.visible;
    }

    // animationDuration -> real duration of the animation, as set in the CSS code. The callback is called after animationDuration.
    // animationRelease -> real animation release (animation class removed). By default, the animation is released as soon as it finishes.
    UIElement.prototype._playAnimation = function(animation, callback = null, animationDuration = 750, animationRelease = 750) {
        var _this = this;
        if (typeof animationDuration === "undefined" || animationDuration === null) {
            animationDuration = 750;
        }
        if (typeof animationRelease === "undefined" || animationRelease === null) {
            animationRelease = animationDuration;
        }
        this.element.addClass(animation);
        if (callback != null && callback instanceof Function) {
            setTimeout(function() {
                callback();
            }, animationDuration);
        }
        setTimeout(function() {
            _this.element.removeClass(animation);
        }, animationRelease);
    }

    UIElement.prototype.slideIn = function(callback, animationDuration = null, animationRelease = null) {
        var animClass = `${this.id}-slide-in`;
        this.show();
        this._playAnimation(animClass, callback, animationDuration, animationRelease);
    }

    UIElement.prototype.slideOut = function(callback, animationDuration = null, animationRelease = null) {
        var animClass = `${this.id}-slide-out`;
        this._playAnimation(animClass, callback, animationDuration, animationRelease);
    }

    function Level(cardId) {
        UIElement.call(this, cardId);
        var _this = this;
        this.user = this.element.find(".user-name");
        this.code = this.element.find(".level-code");
        this.avatar = this.element.find(".user-avatar");
        this.avatarContainer = this.avatar.parent();

        this.avatar.on("load", function() {
            _this.avatarContainer.removeClass("loading");
        });
    }

    Level.prototype = Object.create(UIElement.prototype);
    Level.prototype.constructor = Level;

    Level.prototype.update = function(data) {
        if (data === null) {
            this.user.text('');
            this.code.text('');
        } else {
            if (this.user.text() != data.user) {
                this.avatarContainer.addClass("loading");
                if (data.user in ui.avatarCache) {
                    this.avatar.attr("src", ui.avatarCache[data.user]);
                } else {
                    var _this = this;
                    $.get(apiAvatarEndPoint + data.user, function(response) {
                        ui.avatarCache[data.user] = response;
                        _this.avatar.attr("src", response);
                    });
                }
            }
            this.user.text(data.user);
            this.code.text(data.code);
        }
    }

    Level.prototype.moveToCurrent = function(callback, animationDuration = null, animationRelease = null) {
        if (this.id = 'next-level') {
            this._playAnimation("next-level-to-current", callback, animationDuration, animationRelease);
        }
    }

    var noLevels = new UIElement('no-levels');
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
            if (noLevels.visible) {
                noLevels.slideOut(function() {
                    noLevels.hide();
                }, 1750);
            }
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
                    }, 750, 1000);
                    nextLevel.moveToCurrent(function() {
                        if (hasNext) {
                            nextLevel.update(nextLevelData);
                            nextLevel.slideIn();
                        } else {
                            nextLevel.hide();
                            nextLevel.update(null);
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
                currentLevel.update(null);
                noLevels.slideIn(null, 1750);
            });
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
                frequency: 5,  // Show every X seconds
                duration: 25     // Show for X seconds (ideally, same as the marquee animation duration)
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