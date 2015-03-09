app = angular.module("UserToMovie", ["tastyResource", "ngResource", 'infinite-scroll']);

app.factory("UserToMovie", ["TastyResource", function (TastyResource) {
    return TastyResource({
        url: "/api/v2/user_to_movie/",
        cache: true
    });
}]);


app.controller("UserToMovieController", ["$scope", "UserToMovie", function ($scope, UserToMovie) {



    //$scope.user_to_movies = UserToMovie.query({
    //    'username': 'faito'
    //});
    //$scope.user_to_movie = UserToMovie.get(1);



    //$scope.create = function() {
    //    user_to_movie = UserToMovie;
    //    user.firstname = "John";
    //    user.lastname = "Doe";
    //    user.post();
    //};

    //$scope.edit = function(){
    //    $scope.user.firstname = "Jane";
    //    $scope.user.lastname = "Doe";
    //    $scope.user.put();
    //}
}]);




app.controller("UserToMovieListController", function($scope, Loader) {

    $scope.init = function(username, status) {
        //This function is sort of private constructor for controller
        $scope.loader = new Loader(username, status);
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
            // Success API call
            self.user_to_movies = self.user_to_movies.concat(response.data.objects);
            self.busy = false;
            if (!response.data.meta.next) {
                self.exhausted = true;
            }

        });
    };

    return Loader;
}]);




//app.controller("UserToMovieListController", ["$scope", "UserToMovie", "$resource", function ($scope, UserToMovie, $resource) {
//
//    $scope.user_to_movies = [];
//    var in_progress = false;
//
//    $scope.loadMovies = function() {
//        if (!in_progress) {
//            in_progress = true;
//            UserToMovie.query({
//                'username': 'faito',  // TODO: remove hardcoded stuff
//                'status': 'W',
//                'offset': $scope.user_to_movies.length
//            }, function(response) {
//                // Success API call
//                $scope.user_to_movies = $scope.user_to_movies.concat(response.data.objects);
//                if (!response.data.meta.next) {
//                    in_progress = false;
//                }
//
//            });
//        }
//    };
//
//    //
//    //$scope.user_to_movies = UserToMovie.query({
//    //    'username': 'faito'
//    //});
//
//    $scope.loadMovies();
//
//
//    //$scope.user_to_movie = UserToMovie.get(1);
//
//    //$scope.create = function() {
//    //    user_to_movie = UserToMovie;
//    //    user.firstname = "John";
//    //    user.lastname = "Doe";
//    //    user.post();
//    //};
//
//    //$scope.edit = function(){
//    //    $scope.user.firstname = "Jane";
//    //    $scope.user.lastname = "Doe";
//    //    $scope.user.put();
//    //}
//}]);


//app.directive('whenScrolled', function($window) {
//    return function(scope, element, attrs) {
//        var $myWindow = angular.element($window);
//        $myWindow.bind('scroll', function() {
//            var elementHeight = element.height();
//            var scrollAmount = $myWindow.scrollTop();
//            var delta = 10;
//            //console.log(elementHeight);
//            //console.log(scrollAmount);
//            console.log(elementHeight - (scrollAmount + delta));
//            if (elementHeight - (scrollAmount + delta) < 660) {
//                scope.$apply(attrs.whenScrolled);
//            }
//        });
//
//
//
//
//
//
//        //var raw = elm[0];
//        //
//        //console.log('shit');
//        //
//        //elm.bind('scroll', function() {
//        //    console.log('scrolled');
//        //    if (raw.scrollTop + raw.offsetHeight >= raw.scrollHeight) {
//        //        scope.$apply(attr.whenScrolled);
//        //    }
//        //});
//    };
//});



