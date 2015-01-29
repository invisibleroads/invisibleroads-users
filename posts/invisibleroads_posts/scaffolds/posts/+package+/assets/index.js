require.config({
  paths: {
    common: static_url + 'common'
  }
});
require(['common'], function() {
  console.log('whee');
});
