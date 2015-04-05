app = angular.module("Serp", []);

app.controller("SerpController", ["$scope", "$http", function ($scope, $http) {

    $scope.addMovie = function(movie_id, status) {
        $http.post(
        '/api/v2/user_to_movie/add_movie/',
        {
            movie_id: movie_id,
            status: status
        }).success(function(data, st, headers, config) {
            $scope.status = status;
        });
    };

}]);

