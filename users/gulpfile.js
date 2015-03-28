'use strict';
var argv = require('yargs').argv;
var browserify = require('browserify');
var gulp = require('gulp');
var gulpif = require('gulp-if');
var transform = require('vinyl-transform');
var uglify = require('gulp-uglify');

gulp.task('default', function() {
  return gulp.src('./node_modules/invisibleroads-users/base.js')
    .pipe(transform(function(path) {
      return browserify(path).bundle();
    }))
    .pipe(gulpif(argv.production, uglify()))
    .pipe(gulp.dest('./invisibleroads_users/assets'))
});
