var app = angular.module('ChatApp', []);
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{');
    $interpolateProvider.endSymbol('}');
});


app.controller('chatCtrl', function($scope, $http) {
      $scope.chatData = []
       const person = {
            username: "John",
        };
        $scope.chatData.push(person)
});
