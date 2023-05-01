var app = angular.module('ChatApp', []);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{');
    $interpolateProvider.endSymbol('}');
});


app.controller('chatCtrl', function($scope, $http) {

            $scope.UserData = []
            const person = {
                username: "Karan",
                username1: "jaydip",
                profile: "http://127.0.0.1:8000/static/images/social_media.jpg",
                profile1: "http://127.0.0.1:8000/static/images/nature.jpeg"
            };
            $scope.UserData.push(person)


   $scope.showChat = function(name) {
        $scope.chatData = []

       const data = {
            user: "Chat with "+name,
            name: name,
            chat: "Hi ,This is "+ name,
            chat2 : "hello"

        };
        $scope.chatData.push(data)
        var message = $('.type_msg').val();
        data.chat2 += message;
           }
});


