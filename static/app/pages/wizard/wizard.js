"use strict";
var app = angular.module("Wizard", ["tastyResource", "ngResource", 'cfp.hotkeys']);

app.factory("Suggestion", ["TastyResource", function(TastyResource) {
    return TastyResource({
        url: "/api/v2/movie/get_suggestions/",
        cache: false
    })
}]);

app.run(function($rootScope) {
    $rootScope['T_DID_YOU_WATCH_THIS_MOVIE'] = gettext('Did you watch this movie?');
    $rootScope['T_DIRECTOR'] = gettext('Director');
    $rootScope['T_DIRECTORS'] = gettext('Directors');
    $rootScope['T_STARRING'] = gettext('Starring');
    $rootScope['T_WATCHED'] = gettext('Watched');
    $rootScope['T_PLAN_TO_WATCH'] = gettext('Plan to watch');
    $rootScope['T_IGNORE'] = gettext('Ignore');
    $rootScope['T_THIS_MOVIE_IS_SUGGESTED_TO_YOU_BECAUSE'] = gettext('This movie is suggested to you because');
    $rootScope['T_PART_OF_THE_SERIES_YOU_WATCHED'] = gettext('Part of the series you watched');
    $rootScope['T_TOP_250_IMDB_MOVIE'] = gettext('Top 250 IMDB movie');
});

app.controller("WizardController", ["$scope", "SuggestionLoader", "$http", "hotkeys", function($scope, SuggestionLoader, $http, hotkeys) {

    $scope.init = function() {
        $scope.suggestionLoader = new SuggestionLoader();
        $scope.suggestionLoader.nextBunch();
    };

    $scope.nextMovie = function(movie_id, status) {
        // TODO: success/error callbacks?
        // https://docs.angularjs.org/api/ng/service/$http
        $http.post(
            '/api/v2/user_to_movie/add_movie/',
            {'movie_id': movie_id, 'status': status});

        this.suggestionLoader.suggestions.shift();

        if (this.suggestionLoader.suggestions.length == 0) {
            this.suggestionLoader.nextBunch();
        }
    };

    $scope.gettext = gettext;

    hotkeys.bindTo($scope)
        .add({
          combo: 'w w',
          description: gettext('Mark movie as watched'),
          callback: function() {
              var current_movie = $scope.suggestionLoader.suggestions[0];
              if (current_movie) {
                  $scope.nextMovie(current_movie.id, 'W');
              }
          }
        })
        .add({
          combo: 'p p',
          description: gettext('Mark movie as planned to watch'),
          callback: function() {
              var current_movie = $scope.suggestionLoader.suggestions[0];
              if (current_movie) {
                  $scope.nextMovie(current_movie.id, 'P');
              }
          }
        })
        .add({
          combo: 'space',
          description: gettext('Mark movie as ignored'),
          callback: function() {
              var current_movie = $scope.suggestionLoader.suggestions[0];
              if (current_movie) {
                  $scope.nextMovie(current_movie.id, 'I');
              }
          }
        });
}]);

app.factory('SuggestionLoader', ["TastyResource", "Suggestion", function(TastyResource, Suggestion) {
    var SuggestionLoader = function() {
        this.suggestions = [];
        this.exhausted = false;
        this.busy = false;
        this.bunch_size = 25;
        this.bunch_number = 0;
    };

    SuggestionLoader.prototype.nextBunch = function() {
        if (this.busy) {
            return;
        }

        if (this.exhausted) {
            return;
        }

        this.busy = true;
        var self = this;
        Suggestion.query({}, function(response) {
            // Successful API call
            for (var i = 0, len = response.data.objects.length; i < len; i++) {
                var object = response.data.objects[i];
                object['sort_order'] = self.bunch_number * self.bunch_size + object['suggestion_order'];
                self.suggestions.push(object);
            }
            self.busy = false;
            if (!response.data.objects) {
                self.exhaused = true;
            }
            self.bunch_number++;
        });
    };

    return SuggestionLoader;
}]);
