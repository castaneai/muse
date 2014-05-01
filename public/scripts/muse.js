// $resourceを使うためにはngResourceが必要
var muse = angular.module('muse', ['ngResource']);

muse.service('MuseAudioPlayer', AudioPlayer);

muse.controller('MainCtrl', function($scope, $resource, MuseAudioPlayer) {

    // query()はjson配列形式のデータを取り出す
    //$scope.musics = $resource('/musics').query();
    
    // 今はテスト用のデータを入れる
    $scope.musics = [
        {
            id: 1,
            title: "database",
            url: "musics/1",
            cover: "pictures/1.jpg"
        },
        {
            id: 2,
            title: "Born to be",
            url: "musics/2",
            cover: "pictures/2.jpg"
        }
    ];
    
    $scope.$on('muse.clickItem', function(event, music) {
        // 他の音楽要素に停止状態を知らせる
        $scope.$broadcast('muse.stopItem', music.id);
        // クリックした音楽を再生開始
        MuseAudioPlayer.togglePlay(music.url);
    });
});

/**
 * 1曲を表す要素ディレクティブ
 * クリックすると曲を再生/一時停止できる
 */
muse.directive('museItem', function () {
    return {
        // class="muse-item" の要素に適用されるという意味
        restrict: 'C',
        
        // views/muse-item.htmlが表示されるhtml
        templateUrl: 'views/muse-item.html',
        
        // linkはdirectiveのDOMをjQueryで操れる関数
        // カバー画像と再生状態の見た目に関する部分を記述する
        link: function (scope, element) {
            
            scope.coverIcon = 'play';
            
            element.css('background-image', 'url(' + scope.music.cover + ')');
            
            element.on('mouseover', function() {
                element.find('.cover').show();
            });
            element.on('mouseout', function() {
                element.find('.cover').hide();
            });
            element.on('click', function() {
                scope.coverIcon = (scope.coverIcon == 'play') ? 'pause' : 'play';
                scope.$apply();
                scope.$emit('muse.clickItem', scope.music);
            });
            
            scope.$on('muse.stopItem', function(event, ignoreMusicId) {
                if (scope.music.id !== ignoreMusicId) {
                    scope.coverIcon = 'play';
                    scope.$apply();
                }
            });
        }
    };
});