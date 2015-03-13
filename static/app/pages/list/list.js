app = angular.module("UserToMovie", ["tastyResource", "ngResource", 'infinite-scroll', 'xeditable', "ngRoute"]);

app.factory("UserToMovie", ["TastyResource", function (TastyResource) {
    return TastyResource({
        url: "/api/v2/user_to_movie/",
        cache: true
    });
}]);

app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    $routeProvider
    .when('/', {templateUrl: '/static/app/pages/list/list.html', controller: 'UserToMovieListController'})
    .when('/autism', {templateUrl: '/static/app/pages/list/list_table.html', controller: 'UserToMovieListController'})
    .otherwise({redirectTo: '/'});
}]);

app.run(function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});


app.controller("UserToMovieController", ["$scope", "UserToMovie", function ($scope, $filter) {

    $scope.save = function() {
        $scope.user_to_movie.put();
    };

    $scope.showScore = function() {
        //var selected = $filter('filter')($scope.SCORE_CHOICES, $scope.user_to_movie.score);
        //return ($scope.user_to_movie.score && selected.length) ? selected[0].text : 'Not set';
        return $scope.user_to_movie.score || 'Set score';
    };


}]);


app.controller("UserToMovieListController", function($scope, Loader, $location) {

    $scope.init = function(username, status) {
        //This function is sort of private constructor for controller
        $scope.loader = new Loader(username, status);
        $scope.orderByField = '-id';

        $scope.SCORE_CHOICES = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10
        ];
    };

    $scope.isActive = function(route) {
        return route === $location.path();
    };
});

app.factory('Loader', ["TastyResource", "UserToMovie", function(TastyResource, UserToMovie) {
    var Loader = function(username, status) {
        this.user_to_movies = [];
        this.busy = false;
        this.offset = 0;
        this.exhausted = false;
        this.username = username;
        this.status = status;
    };

    Loader.prototype.nextPage = function() {
        if (this.busy) {
            return;
        }

        if (this.exhausted) {
            return;
        }

        this.busy = true;
        var self = this;
        UserToMovie.query({
            'username': self.username,
            'status': self.status,
            'offset': self.user_to_movies.length
        }, function(response) {
            // Successful API call
            for (var i = 0, len = response.data.objects.length; i < len; i++) {
                self.user_to_movies.push(
                    UserToMovie._create_resource(response.data.objects[i])
                );
            }
            self.busy = false;
            if (!response.data.meta.next) {
                self.exhausted = true;
            }
        });
    };

    return Loader;
}]);
