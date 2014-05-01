var AudioPlayer = (function () {
    
    var currentAudioUrl = null;
    var currentBuzzSound = null;
    
    function AudioPlayer() {
    }
    
    AudioPlayer.prototype.togglePlay = function(audioUrl) {
        if (currentAudioUrl === audioUrl) {
            // 一時停止している曲を再度再生
            togglePlay();
        }
        else {
            // 新しく再生開始
            if (currentBuzzSound !== null) pause();
            currentBuzzSound = new buzz.sound(audioUrl);
            currentAudioUrl = audioUrl;
            play();
        }
    };
    
    function togglePlay() {
        if (currentBuzzSound.isPaused()) {
            play();
        }
        else {
            pause();
        }
    }
    
    function play() {
        currentBuzzSound.fadeIn(1000);
    }
    
    function pause() {
        currentBuzzSound.fadeTo(0, 1000, function() {
            this.pause();
        });
    }
    
    return AudioPlayer;
})();