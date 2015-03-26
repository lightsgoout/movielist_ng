app = angular.module("UserToMovie", ["tastyResource", "ngResource", 'infinite-scroll', 'xeditable', "ngRoute"]);

app.factory("UserToMovie", ["TastyResource", function (TastyResource) {
    return TastyResource({
        url: "/api/v2/user_to_movie/",
        cache: true
    });
}]);

app.factory("Genre", ["TastyResource", function(TastyResource) {
    return TastyResource({
        url: "/api/v2/genre/",
        cache: true
    });
}]);

app.factory("Movie", ["TastyResource", function(TastyResource) {
    return TastyResource({
        url: "/api/v2/movie/",
        cache: true
    });
}]);

app.config(['$routeProvider', '$locationProvider', function($routeProvider) {
    $routeProvider
    .when('/', {templateUrl: '/static/app/pages/list/list.html', controller: 'UserToMovieListController'})
    .when('/table', {templateUrl: '/static/app/pages/list/list_table.html', controller: 'UserToMovieListController'})
    .otherwise({redirectTo: '/'});
}]);

app.run(function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});


app.controller("UserToMovieController", ["$scope", "UserToMovie", function ($scope) {

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


app.controller("ListController", function($scope, Movie) {

    $scope.init = function(person_id, relation) {
        // relation can be one of 'actor' 'director' 'composer' 'writer'
        $scope.orderByField = '-year';

        var kwargs = {
            'limit': 200
        };
        if (relation == 'actor') {
            kwargs['cast'] = person_id;
        } else if (relation == 'director') {
            kwargs['directors'] = person_id;
        }

        $scope.movies = Movie.query(kwargs);
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
        this.first_loading = true;
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
            self.first_loading = false;
        });
    };

    return Loader;
}]);

app.filter('filterByGenre', function () {
    return function (items, genres) {
        var filtered = []; // Put here only items that match
        (items || []).forEach(function (item) { // Check each item
            var matches = genres.some(function (genre) {          // If there is some tag
                return (item.movie.genres.indexOf(tag.text) > -1);
            });                                               // we have a match
            if (matches) {           // If it matches
                filtered.push(item); // put it into the `filtered` array
            }
        });
        return filtered; // Return the array with items that match any tag
    };
});
