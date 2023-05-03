var app = angular.module('ChatApp', []);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
});


app.controller('chatCtrl', function($scope, $http) {

$scope.currentUser = undefined;
$scope.msgText = {text: ""}

        $scope.chatData = [
                {
                id: 1,
                name: "Karan",
                profile: "http://127.0.0.1:8000/static/images/social_media.jpg",
                messages : {
                    sender : [
                    {
                        user: "jaydip",
                        profile: "http://127.0.0.1:8000/static/images/nature.jpeg",
                        message: "hiiii karan this is jaydip [const data]",
                        id: 2
                    }
                    ],
                    receiver : [
                    {
                        user: "karan",
                        profile: "http://127.0.0.1:8000/static/images/social_media.jpg",
                        message: "hiiii karan this is receiver karan",
                        id: 1
                        }
                       ]
                }
            },
            {
                    id: 2,
                    name: "jaydip",
                    profile: "http://127.0.0.1:8000/static/images/nature.jpeg",
                    messages : {
                        sender : [
                        {
                            user: "jaydip",
                            profile: "http://127.0.0.1:8000/static/images/nature.jpeg",
                            message: "hiiii karan this is jaydip",
                            id: 2
                        }
                        ],
                        receiver : [
                        {
                            user: "karan",
                            profile: "http://127.0.0.1:8000/static/images/social_media.jpg",
                            message: "hiii karan this is receiver karan",
                            id: 1
                        }]
                    }
            }

        ]

        $scope.showChat = function(user) {
                $scope.currentUser = user

        };

        $scope.sendChat = function(user){
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

          $scope.status = 'online';
          $scope.setStatus = function(status) {
          console.log(status)
          $scope.status = status;
          }
});
