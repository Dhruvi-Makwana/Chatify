var app = angular.module('ChatApp', []);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
});

app.controller('chatCtrl', function($scope, $http) {
    $scope.userId = $('.userID').text();
    $scope.blockButtonText = "Block";
    var ws = new WebSocket(`${scheme}//${url}/ws/chat/`)
    ws.onopen = function() {}

    $scope.removeOfflineUser = function(chat) {
        $scope.$apply(function() {
            $scope.chatData = $scope.chatData.filter(data => data.id != chat.id);
        });
    }

    $scope.addOnlineUserToList = function(userDetail) {
        if (!$scope.chatData.some(chat => chat.id == userDetail.id)) {
            $scope.$apply(function() {
                $scope.chatData.push(userDetail);
            });
        }
    };
    $scope.isBlocked = {}
    $scope.isBlockedText = {}

    ws.onmessage = function(e, ) {
        let userDetail = JSON.parse(e.data)
        $scope.bloke_user = userDetail.is_blocked
        $scope.$apply(function() {



            if (userDetail.is_blocked == "true") {
                if (userDetail.blocked_user == $scope.currentUser.id) {
                    $scope.isBlocked[userDetail.blocked_user] = true;
                } else if (userDetail.blocked_user == $scope.userId) {
                    $scope.isBlocked[userDetail.blocked_user] = true;

                }
            } else if (userDetail.is_blocked == "false") {
                if (userDetail.blocked_user == $scope.currentUser.id) {
                    $scope.isBlocked[userDetail.blocked_user] = false;


                } else if (userDetail.blocked_user == $scope.userId) {
                    $scope.isBlocked[userDetail.blocked_user] = false;
                }
            } else if (userDetail.user_auth == "logout") {
                loginRedirect()
            } else if (userDetail.data.status == "offline") {
                $scope.removeOfflineUser(userDetail.data);
            } else if (userDetail.data.status == "online") {
                if (userDetail.data.id != $scope.userId) {
                    $scope.addOnlineUserToList(userDetail.data);
                }
            }
        })
    }



    ws.onclose = function(event) {}

    $scope.currentUser = undefined;
    $scope.status = 'online';

    $scope.ajaxGet = function(url, callback = null) {
        $http.get(url).then(function(response) {
            if (callback) {
                callback(response)
            }
        });
    }
    $scope.chatData = []

    $scope.ajaxGet('api/get_online_user/', function(response) {
        $scope.chatData = response.data.UserData;
    })


    $scope.showChat = function(user) {
        if (!user.is_websocket_registered) {
            $scope.ps = new WebSocket(`ws://127.0.0.1:8000/ws/chat/message/${user.id}/`)
            $scope.ps.onopen = function() {}
            $scope.ajaxGet('api/messages/' + user.id, function(response) {
                $scope.data = response.data.messageData;
            })
            $scope.ps.onmessage = function(event) {
                response = JSON.parse(event.data)
                $scope.$apply(function() {
                    $scope.data.push(response)
                })
            }
        }
        user.is_websocket_registered = true
        $scope.currentUser = user
        if ($scope.currentUser.block_user == true) {
            $scope.isBlocked[$scope.currentUser.id] = true;
            $scope.blockButtonText = 'Unblock';
        } else {
            $scope.blockButtonText = 'Block';
        }


    };
    $scope.msgText = {};
    $scope.sendChat = function(user) {

        var message = $scope.msgText[user];
        $scope.msgText[user] = ""
        $scope.date = moment().format('DD/MM/YYYY, hh:mm:ss a');
        $scope.tz = Intl.DateTimeFormat().resolvedOptions().timeZone
        $scope.ps.send(JSON.stringify({
            'msg': message,
            'receiverId': user,
            'senderId': $scope.userId,
            'date': $scope.date,
            'timezone': $scope.tz
        }))

        var currentUser = $scope.chatData.find(function(u) {
            return u.id == user;
        });
    }


    $scope.setStatus = function(status, csrf_token, currentUser_id) {
        $scope.status = status;
        $scope.id = currentUser_id
        var formData = new FormData();
        formData.append('status', $scope.status)
        formData.append('id', $scope.id)
        makeAjaxRequest('POST', csrf_token, "/api/visibility-status/", formData, function(response) {

        })
    }

    $scope.addToBLockList = function(csrf_token, blockUserId) {
        var formData = new FormData();
        $scope.blocked = true
        formData.append('blockUserId', blockUserId)
        makeAjaxRequest('POST', csrf_token, "api/block-user/", formData, function(response) {})
        if ($scope.blockButtonText === 'Block') {
            $scope.blockButtonText = 'Unblock';
        } else {
            $scope.blockButtonText = 'Block';
        }
    }
    $scope.myInterval = setInterval(setUserLastActiveTime, 20000);

    function setUserLastActiveTime() {
        $scope.ajaxGet('api/set-user-active-time/', function(response) {})
    }

    $scope.oneMinuteInterval = setInterval(getUserActiveTime, 60000);

    function getUserActiveTime() {
        $scope.ajaxGet('api/get-user-from-redis/', function(response) {})
    }

});