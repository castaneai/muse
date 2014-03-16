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

var muse = angular.module('muse', ['ngResource']);

muse.controller('MainCtrl', function($scope, $resource) {
    var Musics = $resource('/musics');
    $scope.musics = Musics.query();
});
