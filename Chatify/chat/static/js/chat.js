var app = angular.module('ChatApp', []);

app.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[');
	$interpolateProvider.endSymbol(']}');
});

app.controller('chatCtrl', function($scope, $http) {
	var ws = new WebSocket('ws://127.0.0.1:8000/ws/chat/')

	ws.onopen = function() {
		}
	ws.onmessage = function(e) {

		let userDetail = JSON.parse(e.data)
		if (userDetail.status == "offline") {
			console.log($scope.chatData)
			for (i = 0; i <= $scope.chatData.length; i++) {
				console.log($scope.chatData[i].id)
				if ($scope.chatData[i].id == userDetail.user_id) {
					$scope.chatData.pop(userDetail.user_id)
				}
			}
		}
	}

	function setUserStatus(status) {
		ws.send(JSON.stringify({
			'status': status
		}))
	}

	ws.onclose = function(event) {
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


