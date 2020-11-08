const { description } = require('../../package')

module.exports = {
  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#title
   */
  title: 'Vuepress Docs Boilerplate',
  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#description
   */
  description: description,

  /**
   * Extra tags to be injected to the page HTML `<head>`
   *
   * ref：https://v1.vuepress.vuejs.org/config/#head
   */
  head: [
    ['meta', { name: 'theme-color', content: '#b33939' }],
    ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
    [
      'meta',
      { name: 'apple-mobile-web-app-status-bar-style', content: 'black' },
    ],
  ],

  /**
   * Theme configuration, here is the default theme configuration for VuePress.
   *
   * ref：https://v1.vuepress.vuejs.org/theme/default-theme-config.html
   */
  themeConfig: {
    repo: 'https://github.com/Barbapapazes/dungeons-dragons',
    editLinks: true,
    docsDir: 'docs',
    docsBranch: 'master',
    editLinkText: 'Help us to improve this page !',
    lastUpdated: true,
    nav: [
      {
        text: 'Presentation',
        link: '/presentation/',
      },
      {
        text: 'Config',
        link: '/config/',
      },
      {
        text: 'Guide',
        link: '/guide/',
      },
    ],
    sidebar: {
      '/presentation/': [
        {
          title: 'Presentation',
          collapsable: false,
          children: [''],
        },
      ],
      '/config/': [
        {
          title: 'Configuration',
          collapsable: false,
          children: [''],
        },
      ],
      '/guide/': [
        {
          title: 'Guide',
          collapsable: false,
          children: ['', 'window', 'map_editor'],
        },
      ],
    },
  },

  /**
   * Apply plugins，ref：https://v1.vuepress.vuejs.org/zh/plugin/
   */
  plugins: ['@vuepress/plugin-back-to-top', '@vuepress/plugin-medium-zoom'],
}
