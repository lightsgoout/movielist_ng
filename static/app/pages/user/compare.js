app = angular.module("CompareList", ['angularCharts']);

app.controller("StatsController", ["$scope", "$http", function ($scope, $http) {

    $scope.init = function(first_username, second_username) {

        $http.get(
        '/api/v2/user/stats_comparison/',
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


            var dataPoints = [];
            for (var key in data[first_username]) {
                if (data[first_username].hasOwnProperty(key)) {
                    dataPoints.push(String(data[first_username][key]));
                }
                $scope.scores_data.data.push({
                    x: first_username,
                    y: dataPoints
                });
            }

            dataPoints = [];

            for (var key in data[second_username]) {
                if (data[second_username].hasOwnProperty(key)) {
                    dataPoints.push(String(data[second_username][key]));
                }
                $scope.scores_data.data.push({
                    x: second_username,
                    y: dataPoints
                });
            }



        });


        $scope.scores_config = {
          title: 'Score distribution',
          tooltips: true,
          labels: false,
          legend: {
            display: true,
            //could be 'left, right'
            position: 'right',
            htmlEnabled: true,
          },
          innerRadius: 0, // applicable on pieCharts, can be a percentage like '50%'
          lineLegend: 'lineEnd', // can be also 'traditional'
          colors: [
            '#FF0000', '#FF3400', '#FF5700', '#FF8C00', '#d4a300', '#7f9300',
            '#659300', '#439300', '#21a500', '#12c100']
        };

    };

}]);

