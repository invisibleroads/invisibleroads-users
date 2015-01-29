require.config({
  paths: {
    common: static_url + 'common'
  }
});
require(['common'], function() {
  window.setInterval(function() {
    $('#clock').text((new Date()).getTime());
  }, 1000);
});
