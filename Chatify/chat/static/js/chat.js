var app = angular.module('ChatApp', []);

app.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[');
	$interpolateProvider.endSymbol(']}');
});

app.controller('chatCtrl', function($scope, $http) {
	var ws = new WebSocket('ws://127.0.0.1:8000/ws/chat/my_group/')

	ws.onopen = function() {
		console.log("websocket connection open")
		}

		$scope.remove = function(chat) { 
			var index = $scope.chatData.indexOf(chat);
			$scope.chatData.splice(index, 1);     
		  }



	ws.onmessage = function(e,) {
		console.log("websocket onmessage open")
		let userDetail = JSON.parse(e.data)
		if (userDetail.status == "offline") {
			console.log($scope.chatData)
			for(chat of $scope.chatData) {
				
				if (chat["id"] == userDetail.id) {
					$scope.remove(chat)
					console.log("########")
					console.log($scope.chatData)
					
				}
			}

		}
		else if(userDetail.status == "online")
		{
			 $scope.$apply(function (){
                    $scope.chatData.push(userDetail)
                    });
		}
	}

		function setUserStatus(status) {
		ws.send(JSON.stringify({
			'status': status
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
		makeAjaxRequest('POST', csrf_token, "/api/visibility-status/", formData, function(response) {
			setUserStatus($scope.status)
		})
	}
});


