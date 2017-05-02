/**
 * Created by pratiksanglikar on 21/07/16.
 */
var app = angular.module('idsp');

app.controller("MapController", ["$rootScope", "$scope", "$window", "NgMap", function ($rootScope, $scope, $window, NgMap) {

	NgMap.getMap().then(function (map) {
		console.log(map.getCenter());
		console.log('markers', map.markers);
		console.log('shapes', map.shapes);
	});
	$scope.idsp = "Integrated Disease Surveillance Programme";
}]);