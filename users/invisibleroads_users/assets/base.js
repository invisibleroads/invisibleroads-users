require.config({
  paths: {
    jquery: [
      '//code.jquery.com/jquery-1.11.2.min',
      d.posts.assets_url + 'jquery.min'],
    posts: d.posts.assets_url + 'base'
  } 
});
require(['jquery', 'posts'], function($) {
  // Send CSRF token automatically
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (/^(POST|PUT|DELETE)$/.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader('X-CSRF-Token', d.users.csrf_token);
      }
    }
  });
  // Redirect to login if the page is forbidden
  $(document).ajaxError(function(event, request, settings) {
    if (request.status == 403) {
      window.location = d.users.login_url;
    }
  });
});
