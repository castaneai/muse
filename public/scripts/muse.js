// $resourceを使うためにはngResourceが必要
var muse = angular.module('muse', ['ngResource']);

muse.controller('MainCtrl', function($scope, $resource) {

    // query()はjson配列形式のデータを取り出す
    //$scope.musics = $resource('/musics').query();
    
    // 今はテスト用のデータを入れる
    $scope.musics = [
        {
            id: 1,
            title: "database"
        },
        {
            id: 2,
            title: "Born to be"
        }
    ];
});

/**
 * 1曲を表す要素
 * クリックすると曲を再生/一時停止できる
 */
muse.directive('museItem', function () {
    return {
        // class="muse-item" の要素に適用されるという意味
        restrict: 'C',
        
        // views/muse-item.htmlが表示されるhtml
        templateUrl: 'views/muse-item.html',
        
        // linkはdirectiveのDOMをjQueryで操れる関数
        link: function (scope, element) {
            
            scope.coverIcon = 'play';
            
            element.on('mouseover', function() {
                element.find('.cover').show();
            });
            element.on('mouseout', function() {
                element.find('.cover').hide();
            });
            element.on('click', function() {
                scope.coverIcon = (scope.coverIcon == 'play') ? 'pause' : 'play';
                scope.$apply();
            });
        }
    };
});