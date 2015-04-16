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

app.run(function($rootScope, editableOptions) {
    editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'

    $rootScope['T_WATCHED'] = gettext('Watched');
    $rootScope['T_PLAN_TO_WATCH'] = gettext('Plan to watch');
    $rootScope['T_IGNORED'] = gettext('Ignored');
    $rootScope['T_ADD'] = gettext('Add');
    $rootScope['T_DIRECTOR'] = gettext('Director');
    $rootScope['T_DIRECTORS'] = gettext('Directors');
    $rootScope['T_CAST'] = gettext('Cast');
    $rootScope['T_MY_SCORE'] = gettext('My score');
    $rootScope['T_MY_STATUS'] = gettext('My status');
    $rootScope['T_MOVIE'] = gettext('Movie');
    $rootScope['T_YEAR'] = gettext('Year');
    $rootScope['T_SCORE'] = gettext('Score');
    $rootScope['T_IMDB_RATING'] = gettext('IMDB rating');
    $rootScope['T_IMDB_VOTES'] = gettext('IMDB votes');
    $rootScope['T_DATE_ADDED_ON'] = gettext('Date added on');
    $rootScope['T_ACTIONS'] = gettext('Actions');
    $rootScope['T_DELETE'] = gettext('Delete');
});


app.controller("UserToMovieController", ["$scope", "UserToMovie", "$http", function ($scope, UserToMovie, $http) {

    $scope.setScore = function() {
        $http.post(
        '/api/v2/user_to_movie/set_score/',
        {
            movie_id: $scope.user_to_movie.movie.id,
            score: $scope.user_to_movie.score
        });
    };

    $scope.addMovie = function(movie_id, status) {
        $http.post(
        '/api/v2/user_to_movie/add_movie/',
        {
            movie_id: movie_id,
            status: status
        }).success(function(data, st, headers, config) {
            $scope.user_to_movie.my_status = status;
        });
    };

    $scope.removeMovie = function(movie_id, index) {
        $http.post(
        '/api/v2/user_to_movie/remove_movie/',
        {
            movie_id: movie_id
        }).success(function(data, st, headers, config) {
            $scope.user_to_movie._deleted = true;
        });
    };

    $scope.showScore = function() {
        //var selected = $filter('filter')($scope.SCORE_CHOICES, $scope.user_to_movie.score);
        //return ($scope.user_to_movie.score && selected.length) ? selected[0].text : 'Not set';
        return $scope.user_to_movie.score || gettext('Set score');
    };
}]);

app.controller("FriendshipController", ["$scope", "$http", function($scope, $http) {

    $scope.init = function(username, following) {
        $scope.username = username;
        $scope.following = following;
    };

    $scope.follow = function() {
        $http.post(
        '/api/v2/user/follow/',
        {
            username: $scope.username
        }).success(function() {
            $scope.following = true;
        });
    };

    $scope.unfollow = function() {
        $http.post(
        '/api/v2/user/unfollow/',
        {
            username: $scope.username
        }).success(function() {
            $scope.following = false;
        });
    };

    $scope.getButtonCaption = function() {
        if ($scope.following) {
            return 'Following'
        } else {
            return 'Follow'
        }
    };

    $scope.onClick = function() {
        if ($scope.following) {
            $scope.unfollow();
        } else {
            $scope.follow();
        }
    };
}]);


app.controller("UserToMovieListController", function($scope, Loader, $location) {

    $scope.init = function(username, status, editable, logged_in) {
        //This function is sort of private constructor for controller
        $scope.loader = new Loader(username, status);
        $scope.ordering = '-created_at';

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

        $scope.editable = editable;
        $scope.logged_in = logged_in;
    };

    $scope.isActive = function(route) {
        return route === $location.path();
    };

    $scope.setFilter = function() {
        $scope.loader.setFilter($scope.query);
    };

    $scope.setOrdering = function() {
        $scope.loader.setOrdering($scope.ordering);
    }
});


app.controller("ListController", function($scope, Movie) {

    $scope.init = function(person_id, relation, editable) {
        // relation can be one of 'actor' 'director' 'composer' 'writer'
        $scope.orderByField = '-year';

        var kwargs = {
            'limit': 200
        };
        if (relation == 'actor') {
            kwargs['cast'] = person_id;
        } else if (relation == 'director') {
            kwargs['directors'] = person_id;
        } else if (relation == 'composer') {
            kwargs['composers'] = person_id;
        }

        $scope.loading = true;
        $scope.movies = Movie.query(kwargs, function(response) {
            $scope.loading = false;
        });
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
        this.query = "";
        this.ordering = "";
        this.cast_limit_to = 4;
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

        var kwargs = {
            'username': self.username,
            'status': self.status,
            'offset': self.user_to_movies.length
        };

        if (self.query) {
            kwargs['query'] = self.query;
        }

        if (self.ordering) {
            kwargs['order_by'] = self.ordering;
        }

        UserToMovie.query(kwargs, function(response) {
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

    Loader.prototype.setFilter = function(query) {
        this.query = query;
        this.exhausted = false;
        this.user_to_movies = [];
        if (query) {
            this.cast_limit_to = 100;
        } else {
            this.cast_limit_to = 4;
        }
        this.nextPage();
    };

    Loader.prototype.setOrdering = function(ordering) {
        this.ordering = ordering;
        this.exhausted = false;
        this.user_to_movies = [];
        this.nextPage();
    };

    Loader.prototype.stringMatched = function(string) {
        return this.query && String(string).toLowerCase().search(this.query.toLowerCase()) > -1;
    };

    return Loader;
}]);
