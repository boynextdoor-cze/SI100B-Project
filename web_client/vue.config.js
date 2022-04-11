module.exports = {
  assetsDir: 'static',
  "transpileDependencies": [
    "vuetify"
  ],
  chainWebpack: config => {
    config
      .plugin('html')
      .tap(args =>{
        args[0].title = 'Who is flying over? - SI100B GG Team';
        return args;
      })
  }
}