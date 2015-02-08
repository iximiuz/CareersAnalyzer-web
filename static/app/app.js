var app = angular.module('CareersAnalyzerApp', ['ngMaterial', 'ngTagsInput']);

app.controller('AppCtrl', [function() {

}]);

app.directive('popularSkills', ['$http', '$rootScope', function($http, $rootScope) {
    return {
        restrict: 'E',
        replace: true,
        scope: {},
        link: function(scope, el, attrs) {
            scope.skills = [];
            $http.get('/api/skills/popular').then(function(response) {
                scope.skills = (response || {}).data || [];
            });

            scope.selectSkill = function(skillId) {
                $rootScope.$emit('popular skill selected', skillId);
            };
        },
        templateUrl: '/static/app/partials/popular-skills.html'
    };
}]);

app.directive('analyzer', ['$http', '$rootScope', function($http, $rootScope) {
    return {
        restrict: 'E',
        replace: true,
        scope: {},
        link: function(scope, el, attrs) {
            scope.skills = [];
            scope.jobs = [];
            scope.relatedSkills = [];
            scope.loadSkills = function(query) {
                 return $http.get('/api/skills?q=' + query);
            };

            scope.analyze = function(force) {
                if (!scope.skills.length && true !== force) {
                    scope.jobs = [];
                    scope.relatedSkills = [];
                    return;
                }

                $http.get('/api/analyze?skills=' + encodeURIComponent(_.pluck(scope.skills, 'id').join(',')))
                    .then(function(response) {
                        if ((response.data || {}).skills) {
                            scope.skills = response.data.skills;
                        }

                        if ((response.data || {}).relatedSkills) {
                            scope.relatedSkills = response.data.relatedSkills;
                        }

                        if ((response.data || {}).jobs) {
                            scope.jobs = response.data.jobs;
                        }
                    });
            };

            scope.analyze(true);
        },
        templateUrl: '/static/app/partials/analyzer.html'
    };
}]);