require.config({
  paths: {
    posts: d.posts.assets_url + 'base'
  }
});
require(['posts'], function() {
  window.setInterval(function() {
    $('#clock').text((new Date()).getTime());
  }, 1000);
});
