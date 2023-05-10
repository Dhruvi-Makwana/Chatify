

var app = angular.module('ChatApp', []);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
});


app.controller('chatCtrl', function($scope, $http) {

    $scope.currentUser = undefined;
    $scope.status = 'online';
    $scope.msgText = {
        text: ""
    }
    console.log("webcokds")
    var ws = new WebSocket('ws://127.0.0.1:8000/ws/chat/')

    ws.onopen = function () {
        console.log('websocket conection open')
    }
    ws.onclose = function (event) {
        console.log("message close successfully")
    }

    $scope.ajaxGet = function(url, callback = null) {
        $http.get(url).then(function(response) {
            if (callback) {
                callback(response)
            }
        });
    }

    $scope.chatData = []

    $scope.ajaxGet('api/userdata/', function(response) {
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


    $scope.setStatus = function(status, csrf_token) {
        $scope.status = status;
        var formData = new FormData();
        formData.append('status', $scope.status)
        makeAjaxRequest('POST', csrf_token, "/api/online/", formData, function(response) {})
    }
});



