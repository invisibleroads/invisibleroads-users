({
  appDir: '.',
  baseUrl: 'invisibleroads_posts/assets',
  paths: {
    jquery: 'empty:',
    bootstrap: 'empty:'
  },
  dir: '../../../Experiments/invisibleroads-posts',
  optimize: 'uglify2',
  optimizeCss: 'standard.keepLines',
  removeCombined: true,
  modules: [
    {
      name: 'posts'
    }
  ]
})
