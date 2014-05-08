/**
 * Museの音楽プレイヤー部分
 * 
 * 同時に流れる曲は1曲まで
 */
var AudioPlayer = (function () {
    
    /**
     * 現在再生中の音声のURL
     * @type string
     */
    var currentAudioUrl = null;
    
    /**
     * 現在再生中の音声
     * @type buzz.Sound
     */
    var currentBuzzSound = null;
    
    /**
     * コンストラクタ
     */
    function AudioPlayer() {
    }
    
    /**
     * 指定したURLの音楽の再生/一時停止を切り替える
     * @param string audioUrl 再生する音楽のURL
     */
    AudioPlayer.prototype.togglePlay = function(audioUrl) {
        if (currentAudioUrl === audioUrl) {
            // 一時停止している曲を再度再生
            togglePlay();
        }
        else {
            // 新しく再生開始
            if (currentBuzzSound !== null) pause();
            currentAudioUrl = audioUrl;
            currentBuzzSound = new buzz.sound(audioUrl);
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
        currentBuzzSound.setVolume(0).fadeTo(20, 1000);
    }
    
    function pause() {
        currentBuzzSound.fadeOut(1000);
    }
    
    return AudioPlayer;
})();