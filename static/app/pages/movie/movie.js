app = angular.module("MoviePage", ["tastyResource", "ngResource", 'xeditable', 'ngCookies']);

app.factory("UserToMovie", ["TastyResource", function (TastyResource) {
    return TastyResource({
        url: "/api/v2/user_to_movie/",
        cache: true
    });
}]);

app.run(function($rootScope, editableOptions, $http, $cookies) {
    editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];

    $rootScope['T_NO_COMMENTS'] = gettext('No comments');
});


app.controller("ScoreController", ["$scope", "UserToMovie", "$http", function ($scope, UserToMovie, $http) {

    $scope.showStatus = function() {
        //var selected = $filter('filter')($scope.SCORE_CHOICES, $scope.user_to_movie.score);
        //return ($scope.user_to_movie.score && selected.length) ? selected[0].text : 'Not set';
        var status_text = $scope.STATUSES.filter(function(elem) {
            return elem.id == $scope.user_to_movie.status;
        });
        if (status_text.length) {
            status_text = status_text[0].text;
        } else {
            status_text = null;
        }
        return status_text || gettext('Add to list');
    };

    $scope.showScore = function() {
        //var selected = $filter('filter')($scope.SCORE_CHOICES, $scope.user_to_movie.score);
        //return ($scope.user_to_movie.score && selected.length) ? selected[0].text : 'Not set';
        return $scope.user_to_movie.score || gettext('Set score');
    };

    $scope.save = function() {
        if ($scope.user_to_movie.id) {
            $scope.setStatus();
        } else {
            $scope.addMovie();
        }
    };

    $scope.addMovie = function() {
        $http.post(
        '/api/v2/movie_actions/add_movie/',
        {
            movie_id: $scope.user_to_movie.movie_id,
            status: $scope.user_to_movie.status
        }).success(function(data, status, headers, config) {
            $scope.user_to_movie.id = data.id;
        });
    };

    $scope.setStatus = function() {
        $http.post(
        '/api/v2/movie_actions/set_status/',
        {
            movie_id: $scope.user_to_movie.movie_id,
            status: $scope.user_to_movie.status
        });
    };

    $scope.setScore = function() {
        $http.post(
        '/api/v2/movie_actions/set_score/',
        {
            movie_id: $scope.user_to_movie.movie_id,
            score: $scope.user_to_movie.score
        });
    };

    $scope.setComments = function() {
        $http.post(
        '/api/v2/movie_actions/set_comments/',
        {
            movie_id: $scope.user_to_movie.movie_id,
            comments: $scope.user_to_movie.comments
        });
    };

    $scope.showCommentsHelp = function() {
        $scope.show_comments_help = true;
    };

    $scope.hideCommentsHelp = function() {
        $scope.show_comments_help = false;
    };

    $scope.init = function(movie_id) {
        //This function is sort of private constructor for controller

        $scope.STATUSES = [
            {
                "id": "W",
                "text": gettext("Watched")
            },
            {
                "id": "P",
                "text": gettext("Plan to watch")
            },
            {
                "id": "I",
                "text": gettext("Ignored")
            }
        ];

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

        $http.get(
            '/api/v2/movie_actions/movie_status/',
            {
                params: {
                    'movie_id': movie_id
                }
            }
        ).success(function(data, status, headers, config) {
            $scope.user_to_movie = UserToMovie;
            if (data) {
                $scope.user_to_movie.comments = data.comments;
                $scope.user_to_movie.status = data.status;
                $scope.user_to_movie.score = data.score;
                $scope.user_to_movie.id = data.id;
                $scope.user_to_movie.movie_id = movie_id;
            } else{
                $scope.user_to_movie.status = null;
                $scope.user_to_movie.score = null;
                $scope.user_to_movie.comments = null;
                $scope.user_to_movie.id = null;
                $scope.user_to_movie.movie_id = movie_id;
            }

        });

        $scope.user_to_movie = UserToMovie;
    };


}]);
