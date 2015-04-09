app = angular.module("CompareList", ['n3-pie-chart']);

app.controller("StatsController", ["$scope", "$http", function ($scope, $http) {

    $scope.init = function(username) {
        $http.get(
        '/api/v2/user/stats/',
        {
            params: {
                username: username
            }
        }).success(function(data, st, headers, config) {

            var colors = {
                10: '#12c100',
                9: '#21a500',
                8: '#439300',
                7: '#659300',
                6: '#7f9300',
                5: '#936e00',
                4: '#FF8C00',
                3: '#FF5700',
                2: '#FF3400',
                1: '#FF0000',
            };

            $scope.stats = [];
            for (var key in data) {
                $scope.stats.push({
                    label: String(key),
                    value: data[key],
                    color: colors[key]
                });
              //console.log(key, yourobject[key]);
            }
            console.log($scope.stats);
        });

        $scope.options = {
            thickness: 150
        };
    };

}]);

