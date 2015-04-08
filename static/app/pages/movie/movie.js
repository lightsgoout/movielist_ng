app = angular.module("MoviePage", ["tastyResource", "ngResource", 'xeditable']);

app.factory("UserToMovie", ["TastyResource", function (TastyResource) {
    return TastyResource({
        url: "/api/v2/user_to_movie/",
        cache: true
    });
}]);

app.run(function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
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
            $http.post(
            '/api/v2/user_to_movie/set_score/',
            {
                movie_id: $scope.user_to_movie.movie_id,
                score: $scope.user_to_movie.score
            });
        } else {
            $http.post(
            '/api/v2/user_to_movie/add_movie/',
            {
                'movie_id': $scope.user_to_movie.movie_id,
                'status': $scope.user_to_movie.status
            }).success(function(data, status, headers, config) {
                $scope.user_to_movie.id = data.id;
            });
        }
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
            '/api/v2/user_to_movie/movie_status/',
            {
                params: {
                    'movie_id': movie_id
                }
            }
        ).success(function(data, status, headers, config) {
            $scope.user_to_movie = UserToMovie;
            if (data) {
                $scope.user_to_movie.status = data.status;
                $scope.user_to_movie.score = data.score;
                $scope.user_to_movie.id = data.id;
                $scope.user_to_movie.movie_id = movie_id;
            } else{
                $scope.user_to_movie.status = null;
                $scope.user_to_movie.score = null;
                $scope.user_to_movie.id = null;
                $scope.user_to_movie.movie_id = movie_id;
            }

        });

        $scope.user_to_movie = UserToMovie;
    };


}]);
