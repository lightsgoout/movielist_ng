app = angular.module("UserToMovie", ["tastyResource", "ngResource", 'infinite-scroll', 'xeditable']);

app.factory("UserToMovie", ["TastyResource", function (TastyResource) {
    return TastyResource({
        url: "/api/v2/user_to_movie/",
        cache: true
    });
}]);

app.run(function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});

app.directive("rating", function() {
    var directive = { };
    directive.restrict = 'AE';
    directive.scope = {
        score: '=score',
        max: '=max'
    };
    directive.templateUrl = "/static/app/templates/rating.html";  // TODO: relative path

    directive.link = function(scope, elements, attr) {
        scope.updateStars = function() {
            var idx = 0;
            var max_stars_widget = 5;
            var multiplier = scope.max / max_stars_widget; //
            var star_score = scope.score / multiplier;
            console.log(star_score);
            scope.stars = [];
            var _remaining = star_score;
            for (idx = 0; idx < max_stars_widget; idx += 1) {
                scope.stars.push({
                    full: _remaining >= 1,
                    half_full: _remaining >= 0.5 & _remaining < 1
                });
                _remaining -= 1;
            }
        };

        scope.starClass = function(star, idx) {
            var starClass = 'fa-star-o';
            if(star.half_full) {
                starClass = 'fa-star-half-empty'
            } else if (star.full) {
                starClass = 'fa-star';
            }
            return starClass;
        };

        scope.$watch('score', function(newValue, oldValue) {
          if (newValue !== null && newValue !== undefined) {
            scope.updateStars();
          }
        });

        scope.setRating = function(idx) {
            var max_stars_widget = 5; // todo: duplicate code
            var multiplier = scope.max / max_stars_widget;
            scope.score = idx + 1;
        };
    };




    return directive;
});



app.controller("UserToMovieController", ["$scope", "UserToMovie", function ($scope, $filter) {

    $scope.save = function() {
        $scope.user_to_movie.put();
    };

    $scope.showScore = function() {
        //var selected = $filter('filter')($scope.SCORE_CHOICES, $scope.user_to_movie.score);
        //return ($scope.user_to_movie.score && selected.length) ? selected[0].text : 'Not set';
        return $scope.user_to_movie.score || 'Not set';
    };


}]);


app.controller("UserToMovieListController", function($scope, Loader) {

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
