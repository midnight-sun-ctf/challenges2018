angular.module("pwmeterApp", []).controller('pwmeterController', function($scope, $http, $timeout) {
	$scope.loginstatus = "idle";
	$scope.status = "idle";
	$scope.analysis = "";
	$scope.score = "";

	$scope.sendPassword = function(v) {
		// show spinning disk
		$scope.status = "waiting";
		$timeout(function() {
			var pow = cpwpow(v);
			$http({
			  method: 'GET',
			  url: '/pwmeter/'+v+'/'+pow
			}).then(function (response) {
				// stop spinning disk
				$scope.status = "show";
				$scope.analysis = response.data.analysis;
				$scope.score = response.data.score;
			  }, function (response) {
				// stop spinning disk
				$scope.status = "idle";
				alert("Error");
				console.log(response);
			  });
		}, 100);
	};

	$scope.sendLogin = function(v) {
		$scope.loginstatus = "waiting";
		$timeout(function() {
			var pow = cloginpow(v);
			$http({
			  method: 'GET',
			  url: '/login/'+v+'/'+pow
			}).then(function (response) {
				$scope.loginstatus = "show";
				if(response.data.login) {
					$scope.loginresult = "Login success!";
				} else {
					$scope.loginresult = "Login failed!";
				}
			  }, function (response) {
				$scope.loginstatus = "idle";
				alert("Error");
				console.log(response);
			  });
		}, 100);
	};
});
