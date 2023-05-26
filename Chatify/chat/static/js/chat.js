var app = angular.module('ChatApp', []);

app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
});

app.controller('chatCtrl', function ($scope, $http) {
    $scope.userId = $('.userID').text();

    var ws = new WebSocket('ws://127.0.0.1:8000/ws/chat/')

    ws.onopen = function () {
    }

    $scope.removeOfflineUser = function (chat) {
        $scope.$apply(function () {
            $scope.chatData = $scope.chatData.filter(data => data.id != chat.id);
        });
    }

    $scope.addOnlineUserToList = function (userDetail) {
        if (!$scope.chatData.some(chat => chat.id == userDetail.id)) {
            $scope.$apply(function () {
                $scope.chatData.push(userDetail);
            });
        }
    };
    ws.onmessage = function (e,) {
        let userDetail = JSON.parse(e.data)
        if (userDetail.user_auth == "logout") {
            loginRedirect()
        } else if (userDetail.data.status == "offline") {
            $scope.removeOfflineUser(userDetail.data);
        } else if (userDetail.data.status == "online") {
            $scope.addOnlineUserToList(userDetail.data);
        }
    }

    function setUserStatus(status, id) {
        ws.send(JSON.stringify({
            'status': status,
            'Userid': id,
        }))
    }

    ws.onclose = function (event) {
    }

    $scope.currentUser = undefined;
    $scope.status = 'online';
    $scope.msgText = {
        text: ""
    }


    $scope.ajaxGet = function (url, callback = null) {
        $http.get(url).then(function (response) {
            if (callback) {
                callback(response)
            }
        });
    }
    $scope.chatData = []

    $scope.ajaxGet('api/get_online_user/', function (response) {
        $scope.chatData = response.data.UserData;
    })

    $scope.showChat = function (user) {
        $scope.ps = new WebSocket(`ws://127.0.0.1:8000/ws/chat/message/${user.id}/`)
        $scope.ps.onopen = function () {
        }
        $scope.currentUser = user
    };

    $scope.sendChat = function (user) {
        var message = $scope.msgText.text;
        $scope.ps.onmessage = function (event) {
            response = JSON.parse(event.data)
            $scope.$apply(function () {
                response.isSender = true
                if (currentUser.id == response.id) {
                    response.isSender = false
                }
                currentUser.messages.push(response)
            })
        }

        $scope.ps.send(JSON.stringify({
            'msg': message, 'receiverId': user, 'senderId': $scope.userId
        }))

        var currentUser = $scope.chatData.find(function (u) {
            return u.id == user;
        });
    }


    $scope.setStatus = function (status, csrf_token, currentUser_id) {
        $scope.status = status;
        $scope.id = currentUser_id
        var formData = new FormData();
        formData.append('status', $scope.status)
        makeAjaxRequest('POST', csrf_token, "/api/visibility-status/", formData, function (response) {
            setUserStatus($scope.status, $scope.id)
        })
    }

    $scope.myInterval = setInterval(setUserLastActiveTime, 20000);

    function setUserLastActiveTime() {
        $scope.ajaxGet('api/set-user-active-time/', function (response) {
        })
    }
});