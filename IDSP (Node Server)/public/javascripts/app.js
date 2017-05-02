/**
 * Created by pratiksanglikar on 21/07/16.
 */
var app = angular.module("idsp", ["ngRoute","kendo.directives","ngMap"]);

app.config(function ($routeProvider, $locationProvider) {
	$routeProvider.when("/", {
		templateUrl: "../partials/Map.html",
		controller: "MapController"
	});
	$locationProvider.html5Mode(false);
});