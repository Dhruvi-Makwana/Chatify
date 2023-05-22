var app = angular.module('ChatApp', []);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
});

app.controller('chatCtrl', function($scope, $http) {
    var ws = new WebSocket('ws://127.0.0.1:8000/ws/chat/')

    ws.onopen = function() {
        console.log("websocket connection open")
    }

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
    ws.onmessage = function(e, ) {
        console.log("websocket onmessage open")
        let userDetail = JSON.parse(e.data)
        userDetail.data.status == "offline" ? $scope.removeOfflineUser(userDetail.data) : $scope.addOnlineUserToList(userDetail.data);
        if(userDetail.user_auth == "logout"){
            window.location.href= '/login_page/';
        }
    }

    function setUserStatus(status, id) {
        ws.send(JSON.stringify({
            'status': status,
            'Userid' : id,
        }))
    }

    ws.onclose = function(event) {
        console.log("close event")
    }

    $scope.currentUser = undefined;
    $scope.status = 'online';
    $scope.msgText = {
        text: ""
    }


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
        $scope.currentUser = user

    };

    $scope.sendChat = function(user) {
        var message = $scope.msgText.text;
        var currentUser = $scope.chatData.find(function(u) {
            return u.id === user;
        });
        if (currentUser) {
            currentUser.messages.sender.push({
                user: currentUser.name,
                profile: currentUser.profile,
                message: message,
            });
        }
    }


    $scope.setStatus = function(status, csrf_token, currentUser_id) {
        $scope.status = status;
        $scope.id = currentUser_id
        var formData = new FormData();
        formData.append('status', $scope.status)
        makeAjaxRequest('POST', csrf_token, "/api/visibility-status/", formData, function(response) {
            setUserStatus($scope.status, $scope.id)
        })
    }
});