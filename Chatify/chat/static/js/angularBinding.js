var app = angular.module('ChatApp', []);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{');
    $interpolateProvider.endSymbol('}');
});


app.controller('chatCtrl', function($scope, $http) {
      $scope.chatData = []
      $scope.UserData = []
       const data = {
            chat: "Hi ,Data binding with Angular JS",

        };
        $scope.chatData.push(data)

       const person = {
            username: "Karan"
            username1: "jaydip"
        };
        $scope.UserData.push(person)

});

