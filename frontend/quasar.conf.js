const { configure } = require('quasar/wrappers');

module.exports = configure(function (ctx) {
  return {
    supportTS: false,
    boot: [
      'base',
    ],
    css: [
      'app.scss'
    ],
    extras: [
      'fontawesome-v5',
      'roboto-font',
    ],
    build: {
      vueRouterMode: 'history',
      chainWebpack (/* chain */) { },
    },
    devServer: {
      https: false,
      port: 8080,
      open: true
    },
    framework: {
      config: {},
      iconSet: 'fontawesome-v5',
      lang: 'ru',
      plugins: ['Notify']
    },
    animations: [],
    ssr: {
      pwa: false,
      prodPort: 3000,
      maxAge: 1000 * 60 * 60 * 24 * 30,
      chainWebpackWebserver (/* chain */) { },
      middlewares: [
        ctx.prod ? 'compression' : '',
        'render'
      ]
    },
    pwa: {
      workboxPluginMode: 'GenerateSW',
      workboxOptions: {},
      chainWebpackCustomSW (/* chain */) { },
      manifest: {
        name: `Quasar App`,
        short_name: `Quasar App`,
        description: `A Quasar Framework app`,
        display: 'standalone',
        orientation: 'portrait',
        background_color: '#ffffff',
        theme_color: '#027be3',
        icons: [
          {
            src: 'icons/icon-128x128.png',
            sizes: '128x128',
            type: 'image/png'
          },
          {
            src: 'icons/icon-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'icons/icon-256x256.png',
            sizes: '256x256',
            type: 'image/png'
          },
          {
            src: 'icons/icon-384x384.png',
            sizes: '384x384',
            type: 'image/png'
          },
          {
            src: 'icons/icon-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }
    },
    cordova: {},
    capacitor: {
      hideSplashscreen: true
    },
    electron: {
      bundler: 'packager',
      packager: {},
      builder: {
        appId: 'frontend'
      },
      chainWebpackMain (/* chain */) { },
      chainWebpackPreload (/* chain */) { },
    }
  }
});
