var sampleApp = angular.module('sampleApp', ['ngRoute']);

// Routing
sampleApp.config(['$routeProvider', function($routeProvider) {
	$routeProvider
		.when('/Home', {
			templateUrl: 'static/partials/home.html',
			controller: 'HomeController as homeCtrl'
		})
		.when('/Studio/:selectedYear', {
			templateUrl: 'static/partials/studio.html',
			controller: 'StudioController as studioCtrl'
		})
		.when('/CustomPlaylist/:plid', {
			templateUrl: 'static/partials/cplaylist.html',
			controller: 'CustomPlaylistController as cplaylistCtrl'
		})
		.otherwise({
			redirectTo: '/Home'
		});
}]);

// Controllers
sampleApp.controller('HomeController', ['$location', function($location) {
	var self = this;
	self.years = [];

	for (i = 2000; i < 2015; i++) {
		self.years.push(i);
	}

	self.goToYear = function() {
		var theYear = $('#theYear').val().trim();
		$location.path('/Studio/' + theYear);
	}
}]);

sampleApp.controller('StudioController', ['$routeParams', '$http', '$scope', function($routeParams, $http, $scope) {
	var self = this;
	var rp = $routeParams.selectedYear;
	self.data = [];

	self.custom = []

	var id = 'data12';

	$(document).on('submit', '#new-pl-form', function(event){
		event.preventDefault();
		var plname = $('#plname', this).val();
		$http.post('/new-playlist', {"list_name": plname})
			.success(function(data, status) {
				console.log(data);
				$('#custom-plist').append('<div style="background-color:#F5D0A9;padding:3px;margin-bottom:3px;"><a href="#/CustomPlaylist/'+data.id+'">#'+plname+'</a></div>');
			});
		$.fancybox.close();
		return false;
	});

	/*
	$(".inline").click(function(e) {
		id = $(this).attr('value');
		alert(id);

		$("a.inline").fancybox({
			'content': $('#'+ id).html(),
			'hideOnContentClick': true
		});
		
	});

	*/
	


	$scope.$watch(function ngModelWatch() {
		$(".inline").click(function(e) {
			id = $(this).attr('value');
			//var html = '<div><iframe width="280" height="200" src="https://www.youtube.com/embed/'+id+'" frameborder="0" allowfullscreen></iframe></div>';
			//$('#'+ id).append(html);
			$("a.inline").fancybox({
				'content': $('#'+ id).html(),
				'hideOnContentClick': true
			});
			
		});

	});

	 

	
	


	$http.get('/songs')
		.success(function(data, status, headers, config) {
			$('#loading').hide();
			$.each(data.data, function(index, element) {
				//$('#theYear').hide();
				element['imgsrc'] = 'http://i.ytimg.com/vi/' + element.code + '/hqdefault.jpg';
				element['ysrc'] = 'https://www.youtube.com/watch?v=' + element.code;
				self.data.push(element);
			});
			//console.log($.map(self.data, function(x) {return x.code;}));
			var ls = $.map(self.data, function(x) {return x.code;});
			$('#playAll').click(function(){
			 	if (true || player.getPlayerState() !== 1) {
			 		$('#player').show('slow');
			 		$('#current-playing').append('<h1>'+rp+'</h1>');
			 		player.loadPlaylist(ls);
			 	}

			 });
			//if (player.getPlayerState() !== 1) {
				console.log('Loading playlist');
				//player.loadPlaylist(ls);//['QC5ZwfzVPR0', 'hRarRMOmKq4'])
			//}
			
		})
		.error(function(data, status, headers, config) {
			console.log('Something goes wrong while requesting /songs');
		});


		$http.get('/custom-playlist')
			.success(function(data, status, headers, config) {
				$.each(data.data, function(index, element) {
					element['src'] = '#/CustomPlaylist/' + element.id
					self.custom.push(element);
				});
			})
			.error(function(data, status, headers, config) {
				console.log('Something goes wrong while requesting /songs');
			});

}]);

sampleApp.controller('SocialController', ['$http', function($http) {
	var self = this;
	
	self.data = [];



	$http.get('/facebook')
		.success(function(data, status, headers, config) {
			$.each(data.data, function(index, element) {
				element['src'] = 'https://www.facebook.com/' + element['idd'];
				self.data.push(element);
			});
		})
		.error(function(data, status, headers, config) {
			
		});
}]);

sampleApp.controller('CustomPlaylistController', ['$scope', '$http',  '$routeParams', function($scope, $http, $routeParams) {
	var self = this;
	var plid = $routeParams.plid;
	self.years = ['rat'];

	self.clips = [];

	$http.get('/one-playlist/' + plid)
		.success(function(data, status, headers, config) {
			self.current = data.data;
		})
		.error(function(data, status, headers, config) {
			
		});

	$http.get('/get-all-clips/' + plid)
		.success(function(data, status, headers, config) {
			console.log(data.data);
			$.each(data.data, function(index, element) {
				element['imgsrc'] = 'http://img.youtube.com/vi/'+element.code+'/hqdefault.jpg';
				self.clips.push(element);
			});
		})
		.error(function(data, status, headers, config) {
			alert(89);
		});


	$scope.$watch(function ngModelWatch() {
		
		$(".inline").click(function(e) {
			id = $(this).attr('value');
			//var html = '<div><iframe width="280" height="200" src="https://www.youtube.com/embed/'+id+'" frameborder="0" allowfullscreen></iframe></div>';
			//$('#'+ id).append(html);
			$("a.inline").fancybox({
				'content': $('#'+ id).html(),
				'hideOnContentClick': true
			});
			
		});

	});


	$(document).on('submit', '#add-new-clip', function(event){
		event.preventDefault();
		
		var idd = $('#idd', this).val();
		var clname = $('#clipname', this).val();
		

		$http.post('/new-clip', {"clip_name": clname, 'id': idd})
			.success(function(data, status) {
				
				data['title'] = 'TITLE';
				data['ysrc'] = clname;
				data['code'] = data['vid'];
				data['imgsrc'] = 'http://img.youtube.com/vi/'+data.vid+'/hqdefault.jpg';
				
				self.clips.push(data);
				$('#cllist').append('');
				console.log(data);
			});
		$.fancybox.close();
	});

	
}]);