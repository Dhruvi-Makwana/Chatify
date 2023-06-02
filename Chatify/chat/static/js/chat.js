var app = angular.module('ChatApp', []);

app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
});

app.controller('chatCtrl', function ($scope, $http) {
    $scope.userId = $('.userID').text();
    var ws = new WebSocket(`${scheme}//${url}/ws/chat/`)
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
            if (userDetail.data.id != $scope.userId) {
                $scope.addOnlineUserToList(userDetail.data);
            }
        }
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
         $scope.ajaxGet('api/messages/' + user.id, function (response) {
              $scope.data = response.data.messageData;

         })
         $scope.currentUser = user
         $scope.ps = new WebSocket(`${scheme}//${url}/ws/chat/message/${user.id}/`)
         $scope.ps.onmessage = function (event) {
            response = JSON.parse(event.data)
            $scope.$apply(function () {
                $scope.data.push(response)
            })
        }
    };

    $scope.sendChat = function (user) {
        var message = $scope.msgText.text;
        $scope.msgText.text = " "

        $scope.date = moment().format('DD/MM/YYYY, hh:mm:ss a');
        $scope.tz = Intl.DateTimeFormat().resolvedOptions().timeZone
        $scope.ps.send(JSON.stringify({
            'msg': message, 'receiverId': user, 'senderId': $scope.userId, 'date' : $scope.date, 'timezone' : $scope.tz
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
        formData.append('id', $scope.id)
        makeAjaxRequest('POST', csrf_token, "/api/visibility-status/", formData, function (response) {

        })
    }

    $scope.myInterval = setInterval(setUserLastActiveTime, 20000);

    function setUserLastActiveTime() {
        $scope.ajaxGet('api/set-user-active-time/', function (response) {
        })
    }

    $scope.oneMinuteInterval = setInterval(getUserActiveTime, 60000);

    function getUserActiveTime() {
        $scope.ajaxGet('api/get-user-from-redis/', function (response) {
        })
    }

});