// Include gulp
var gulp = require('gulp');

// Include Our Plugins
var jshint = require('gulp-jshint');
var sass = require('gulp-sass');
// var sourcemaps  = require('gulp-sourcemaps');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var minify = require('gulp-minify');
var gutil = require('gulp-util');
var cleanCSS = require('gulp-clean-css');

// Lint Task
gulp.task('lint', function() {
    return gulp.src('digitaloxford/static/js/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

// Compile our Sass and concatenate & minify CSS
gulp.task('styles', function() {
    return gulp.src('scss/main.scss')
        // .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(cleanCSS())
        .pipe(concat('digitaloxford.css'))
        // .pipe(sourcemaps.write())
        .pipe(gulp.dest('digitaloxford/static/css'));
});

// Concatenate & Minify JS
gulp.task('scripts', function() {
    return gulp.src([
        'js/jquery.min.js',
        'js/site.js'
    ])
    .pipe(concat('all.js'))
    .pipe(uglify())
    .pipe(rename('digitaloxford.js'))
    .pipe(gulp.dest('digitaloxford/static/js'));
});

gulp.task('serviceworker', () => {
    // TODO: Rebuild serviceworker after changes.
})

// Watch Files For Changes
gulp.task('watch', function() {
    gulp.watch('js/**/*.js', gulp.series('scripts'));
    gulp.watch('scss/**/*.scss', gulp.series('styles'));
    // gulp.watch([
    //     'htdocs/js/**/*.js',
    //     'htdocs/css/**/*.css',
    //     'htdocs/*.png',
    //     'htdocs/*.ico',
    //     'htdocs/img/**/*'
    // ], gulp.series('serviceworker'));
});

// Default Task
gulp.task('default', gulp.series('lint', 'styles', 'scripts', 'watch'));
