$(function() {
  // Get stylesheets if CDNs failed
  if ($('body').css('color') != 'rgb(51, 51, 51)') {
    $('head').append('<link rel="stylesheet" href="' + d.posts.assets_url + 'bootstrap.min.css">');
  }
});
