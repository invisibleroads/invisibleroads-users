require.config({
  paths: {
    jquery: [
      '//code.jquery.com/jquery-1.11.2.min',
      d.posts.assets_url + 'jquery.min'],
    posts: d.posts.assets_url + 'base'
  } 
});
require(['jquery', 'posts'], function($) {
  // Send csrf_token automatically for POST requests
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if ('POST' != settings.type) return;
      xhr.setRequestHeader('X-CSRF-Token', d.users.csrf_token);
    }
  });
  // Redirect to login if the page is forbidden
  $(document).ajaxError(function(event, request, settings) {
    if (request.status == 403) window.location = d.users.login_url;
  });
});
