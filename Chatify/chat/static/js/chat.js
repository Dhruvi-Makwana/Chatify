var app = angular.module('ChatApp', []);

app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
});

app.controller('chatCtrl', function ($scope, $http) {
    var ws = new WebSocket('ws://127.0.0.1:8000/ws/chat/')

    ws.onopen = function () {
        console.log("websocket connection open")
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
        console.log("websocket onmessage open")
        let userDetail = JSON.parse(e.data)
        userDetail.status == "offline" ? $scope.removeOfflineUser(userDetail) : $scope.addOnlineUserToList(userDetail);
    }

    function setUserStatus(status) {
        ws.send(JSON.stringify({
            'status': status
        }))
    }

    ws.onclose = function (event) {
        console.log("close event")
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
            console.log("websocket connection open for chat")
        }
        $scope.currentUser = user
    };

    $scope.sendChat = function (user) {
        var message = $scope.msgText.text;
        $scope.ps.onmessage = function (event) {
            response = JSON.parse(event.data)

            $scope.$apply(function () {
                if (currentUser.id != response[0].sendId) {
                    response.isSender = true

                    currentUser.messages.push({
                        "isSender": true,
                        "message": response[0].message,
                        "profile": response[0].profile,
                    })

                    console.log(currentUser)
                }
                else {
                    response.isSender = false
                    currentUser.messages.push({
                        "isSender": false,
                        "message": response[0].message,
                        "profile": response[0].profile,
                    })
                    console.log(currentUser)

                }
            })
        }

        $scope.userId = $('.userID').text();
        $scope.ps.send(JSON.stringify({
            'msg': message, 'receiverId': user, 'senderId': $scope.userId
        }))

        var currentUser = $scope.chatData.find(function (u) {
            return u.id == user;
        });

        // if (currentUser) {
        //     $scope.data.sender[0].push({
        //         user: currentUser.name,
        //         profile: currentUser.profile,
        //         message: message,
        //     });
        // }
    }


    $scope.setStatus = function (status, csrf_token) {
        $scope.status = status;
        var formData = new FormData();
        formData.append('status', $scope.status)
        makeAjaxRequest('POST', csrf_token, "/api/visibility-status/", formData, function (response) {
            setUserStatus($scope.status)
        })
    }
});