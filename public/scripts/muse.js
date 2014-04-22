/*
function sendFile(file) {
    var formData = new FormData();
    formData.append('upload', file);

    var options = {
        method: 'POST',
        url: '/upload',
        data: formData,
        processData: false,
        contentType: false,
        error: function() {
            console.log('file upload error');
        },
        success: function() {
            console.log('success upload!');
        }
    };

    $.ajax('/upload', options);
}

$(document).ready(function() {

    var cancelEvent = function(e) {
        e.preventDefault();
    };

    $(document)
    .on('dragenter', cancelEvent)
    .on('dragover', cancelEvent)
    .on('drop', function(e) {
        cancelEvent(e);
        var files = e.originalEvent.dataTransfer.files;

        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            console.dir(file);

            if (file.type.match("audio")) {
                console.log('send file: ' + file.name);
                sendFile(file);
            }
        }
    });
});
*/

// $resourceを使うためにはngResourceが必要
var muse = angular.module('muse', ['ngResource']);

muse.service('AudioPlayer', function() {
    var audio = null;
    var currentMusicId = -1;
    
    this.play = function(musicId) {
        if (musicId === currentMusicId) {
            if (audio.paused) {
                audio.play();
            }
            else {
                audio.pause();
            }
        }
        else {
            if (audio !== null) {
                audio.pause();
            }
            audio = new Audio('./musics/' + musicId);
            audio.play();
            currentMusicId = musicId;
        }
    };
});

muse.controller('MainCtrl', function($scope, $resource, AudioPlayer) {
    
    var MusicAPI = $resource('/musics');
    
    // query()はjson配列形式のデータを取り出す
    //$scope.musics = MusicAPI.query();
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
    
    $scope.canPlay = {};
    
    $scope.play = function(musicId) {
        AudioPlayer.play(musicId);
    };
});
