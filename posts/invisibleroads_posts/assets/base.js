requirejs.config({
  paths: {
    jquery: [
      '//code.jquery.com/jquery-1.11.2.min',
      d.posts.assets_url + 'jquery.min'],
    bootstrap: [
      '//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min',
      d.posts.assets_url + 'bootstrap.min']}});
require(['jquery', 'bootstrap'], function($) {
  // Get stylesheets if CDNs failed
  if ($('body').css('color') != 'rgb(51, 51, 51)') {
    $('head').append('<link rel="stylesheet" href="' + d.posts.assets_url + 'bootstrap.min.css">');
  }
});
