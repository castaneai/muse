// $resourceを使うためにはngResourceが必要
var muse = angular.module('muse', ['ngResource', 'angularFileUpload']);

muse.service('MuseAudioPlayer', AudioPlayer);

muse.controller('MainCtrl', function($scope, $resource, $upload, MuseAudioPlayer) {
    
    function loadMusics() {
        // query()はjson配列形式のデータを取り出す
        $scope.musics = $resource('/musics').query();
    }

    loadMusics();

    $scope.$on('muse.clickItem', function(event, music) {
        // 他の音楽要素に停止状態を知らせる
        $scope.$broadcast('muse.stopItem', music.id);
        // クリックした音楽を再生開始
        MuseAudioPlayer.togglePlay(music.audio_url);
    });

    $scope.upload = function(file) {
        $upload.upload({
            url: 'upload',
            file: file
        })
        .success(function(result) {
            console.log('%s was uploaded.', result.name);
            loadMusics();
            $scope.$apply();
        })
        .error(function() {
            console.error('upload failed.');
        });
    };

    $scope.onFileDrop = function($files) {
        console.dir($files);
        for (var i = 0; i < $files.length; i++) {
            $scope.upload($files[i]);
        }
    };
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

            // 最初は再生ボタンを表示するように
            scope.coverIcon = 'play';

            // カバー画像を付ける
            element.css('background-image', 'url(' + scope.music.cover_url + ')');

            // マウスカーソルを合わせると再生 or 一時停止ボタンが
            // うっすらと現れる
            element.on('mouseover', function() {
                element.find('.cover').show();
            });
            element.on('mouseout', function() {
                element.find('.cover').hide();
            });

            // クリックすると再生/一時停止が実行される
            // しかしこのスコープ内は見た目だけを処理したいので
            // この曲をクリックしたというイベントを親のコントローラに丸投げする
            element.on('click', function() {
                scope.coverIcon = (scope.coverIcon == 'play') ? 'pause' : 'play';
                scope.$apply();
                scope.$emit('muse.clickItem', scope.music);
            });

            // 親のコントローラから「停止状態の見た目に変えろ」というイベントが
            // 来たら停止状態の見た目にかえる
            scope.$on('muse.stopItem', function(event, ignoreMusicId) {
                if (scope.music.id !== ignoreMusicId) {
                    scope.coverIcon = 'play';
                    scope.$apply();
                }
            });
        }
    };
});