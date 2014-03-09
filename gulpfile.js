var gulp = require('gulp');
var gutil = require('gulp-util');

// ファイル監視・自動リロード系
var watch = require('gulp-watch');
var connect = require('gulp-connect');

// CSS関連
var less = require('gulp-less');

// 設定
var dir = {
    src: './public', // ドキュメントルートであり，ソースコードが置かれる
    tmp: './.tmp' // コンパイルで生成されたcssやjsファイルが置かれる
};

gulp.task('html', function() {
    gulp.src(dir.src + '/*.html')
        .pipe(connect.reload());
});

gulp.task('less', function() {
    gulp.src(dir.src + '/styles/*.less')
        .pipe(less())
        .pipe(gulp.dest(dir.tmp + '/styles'))
        .pipe(connect.reload());
});

gulp.task('js', function() {
    gulp.src(dir.src + '/scripts/*.js')
        .pipe(connect.reload());
});

gulp.task('connect', connect.server({
    root: [dir.src, dir.tmp],
    port: 9000,
    livereload: true,
    open: { browser: 'chrome' }
}));

gulp.task('watch', function() {
    gulp.watch([dir.src + '/*.html'], ['html']);
    gulp.watch([dir.src + '/styles/*.less'], ['less']);
    gulp.watch([dir.src + '/scripts/*.js'], ['js']);
});

gulp.task('default', ['connect', 'watch']);