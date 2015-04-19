app = angular.module("Serp", ["ngCookies"]);

app.run(function($http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
});

app.controller("SerpController", ["$scope", "$http", function ($scope, $http) {

    $scope.addMovie = function(movie_id, status) {
        $http.post(
        '/api/v2/movie_actions/add_movie/',
        {
            movie_id: movie_id,
            status: status
        }).success(function(data, st, headers, config) {
            $scope.status = status;
        });
    };

}]);

