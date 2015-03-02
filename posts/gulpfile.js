'use strict';

var browserify = require('browserify');
var gulp = require('gulp');
var transform = require('vinyl-transform');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');

gulp.task('javascript', function () {
  var browserified = transform(function(filename) {
    var b = browserify(filename);
    return b.bundle();
  });

  return gulp.src('./invisibleroads_posts/modules/base.js')
    .pipe(browserified)
    .pipe(sourcemaps.init({loadMaps: true}))
        .pipe(uglify())
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest('./invisibleroads_posts/assets/base.js'));
});

gulp.task('default', ['javascript']);
