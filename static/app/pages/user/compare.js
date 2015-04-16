app = angular.module("CompareList", ['angularCharts']);

app.controller("StatsController", ["$scope", "$http", function ($scope, $http) {

    $scope.init = function(first_username, second_username) {

        $http.get(
        '/api/v2/list_comparison/stats_comparison/',
        {
            params: {
                first_username: first_username,
                second_username: second_username
            }
        }).success(function(data, st, headers, config) {
            $scope.scores_data = {
                series: ['&nbsp;1', '&nbsp;2', '&nbsp;3', '&nbsp;4', '&nbsp;5', '&nbsp;6', '&nbsp;7', '&nbsp;8', '&nbsp;9', '&nbsp;10'],
                data: []
            };

            var SCORES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

            var dataPoints = [];
            var tooltips = [];

            for (var key in SCORES) {
                var score = SCORES[key];
                if (data[first_username].hasOwnProperty(score)) {
                    dataPoints.push(String(data[first_username][score]));
                    tooltips.push(String(score) + ' used ' + data[first_username][score] + ' times');
                } else {
                    dataPoints.push(0);
                    tooltips.push('0');
                }
            }
            $scope.scores_data.data.push({
                x: first_username,
                y: dataPoints,
                tooltip: tooltips
            });

            dataPoints = [];
            tooltips = [];

            for (key in SCORES) {
                score = SCORES[key];
                if (data[second_username].hasOwnProperty(score)) {
                    dataPoints.push(String(data[second_username][score]));
                    tooltips.push(String(score) + ' used ' + data[second_username][score] + ' times');
                } else {
                    dataPoints.push(0);
                    tooltips.push('0');
                }
            }

            $scope.scores_data.data.push({
                x: second_username,
                y: dataPoints,
                tooltip: tooltips
            });
        });


        $scope.scores_config = {
          title: 'Score distribution',
          tooltips: true,
          labels: false,
          legend: {
            display: true,
            //could be 'left, right'
            position: 'right',
            htmlEnabled: true
          },
          innerRadius: 0, // applicable on pieCharts, can be a percentage like '50%'
          lineLegend: 'lineEnd', // can be also 'traditional'
          colors: [
            '#FF0000', '#FF3400', '#FF5700', '#FF8C00', '#d4a300', '#7f9300',
            '#659300', '#439300', '#21a500', '#12c100']
        };

    };
}]);

app.controller("ListController", function($scope, $http) {

    $scope.init = function(first_username, second_username, mode) {
        // mode can be one of 'S' 'L' 'R'
        var url = '';
        if (mode == 'S') {
            url = '/api/v2/list_comparison/shared_with/';
        } else if(mode == 'L') {
            url = '/api/v2/list_comparison/unique_left/'
        } else if(mode == 'R') {
            url = '/api/v2/list_comparison/unique_right/'
        }

        $scope.loading = true;

        $http.get(
        url,
        {
            params: {
                first_username: first_username,
                second_username: second_username
            }
        }).success(function(data, st, headers, config) {
            $scope.user_to_movies = data;
            $scope.loading = false;
        });

        $scope.mode = mode;

    };


});
