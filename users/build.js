({
  appDir: '.',
  baseUrl: 'invisibleroads_users/assets',
  paths: {
    jquery: 'empty:',
    posts: 'empty:'
  },
  dir: '../../../Experiments/invisibleroads-users',
  optimize: 'uglify2',
  optimizeCss: 'standard.keepLines',
  removeCombined: true,
  modules: [
    {
      name: 'base'
    }
  ]
})
