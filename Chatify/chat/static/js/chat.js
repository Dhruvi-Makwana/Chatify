var app = angular.module('ChatApp', []);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{');
    $interpolateProvider.endSymbol('}');
});


app.controller('chatCtrl', function($scope, $http) {

$scope.currentUser = undefined;


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
        console.log($scope.chatData)


    $scope.showChat = function(user) {
            $scope.currentUser = user
            console.log($scope.currentUser)
    };

    $scope.sendChat = function(user){
     var message = $scope.msgText;
        alert($scope.msgText)
        console.log(user)
        console.log($scope.chatData[1].id)

        var a = $scope.chatData[1].id
        if(user == a)
        {
            var text = $scope.msgText;
            $scope.chatData[1].messages.sender.push(message);
        }
    }

});


