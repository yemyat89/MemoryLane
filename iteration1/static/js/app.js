var my_app = angular.module('MemoryLaneApp', ['ngRoute']);


// Routing
my_app.config(['$routeProvider', function($routeProvider) {
  $routeProvider
    .when('/Home', {
      templateUrl: 'static/partials/home.html',
      controller: 'HomeController as ctrl'
    })
    .when('/Studio/:selected_year/:media_type', {
      templateUrl: 'static/partials/studio.html',
      controller: 'StudioController as ctrl'
    })
    .otherwise({
      redirectTo: '/Home'
    });
}]);
// -------------------------------------------------------------


// Controllers
my_app.controller('HomeController', ['$location', function($location) {
  var self = this;
  self.years_display = [];

  for (i = 1960; i < 2015; i++) {
    self.years_display.push(i);
  }


  if (player !== 0 && player !== undefined) {
    $("#player_container").hide();
    if (player.getPlayerState() == 1) {
      player.stopVideo();
    }
  }

  self.goToYear = function() {
    var selected_year = $('#selected_year').val().trim();
    $location.path('/Studio/' + selected_year + '/songs');
  }
}]);

my_app.controller('StudioController', ['$routeParams', '$http', '$scope', function($routeParams, $http, $scope) {
  var self = this;
  
  self.selected_year = $routeParams.selected_year;
  self.media_type = $routeParams.media_type;

  self.songs_url = '#/Studio/' + self.selected_year + '/songs';
  self.movies_url = '#/Studio/' + self.selected_year + '/movies';

  self.clips = [];


  // TODO: Move to a service
  var request_url = '/';
  if (self.media_type == 'movies') {
    request_url += 'movies/';
    self.type_title = 'Movies';
  }
  else{
    request_url += 'songs/';
    self.type_title = 'Songs';
  }
  request_url += self.selected_year;
  $http.get(request_url)
    .success(function(data, status, headers, config) {
      $.each(data.result, function(index, element){
        element['title'] = element['title']
        element['youtube_url'] = 'http://youtube.com/watch?v=' + element.youtube_code;
        element['youtube_thumbnail'] = 'http://img.youtube.com/vi/' + element.youtube_code + '/hqdefault.jpg';
        self.clips.push(element);
      });
    })
    .error(function(data, status, headers, config) {
      console.log('Something goes wrong while requesting ' + request_url);
    });
    

    // Click event handlers
    $('#play_all').click(function(event){
      $('#player_container').show();
      var ls = $.map(self.clips, function(item){
        return item.youtube_code;
      });
      player.loadPlaylist(ls);
    });


    // Fancybox register
    $scope.$watch(function ngModelWatch() {
      $(".inline").click(function(e) {
        var id = $(this).attr('value');
        console.log(id);
        $("a.inline").fancybox({
          'content': $('#'+ id).html(),
          'hideOnContentClick': true
        });
      });
    });
  
}]);
// -------------------------------------------------------------


// jQuery document ready
$(document).ready(function() {

});


