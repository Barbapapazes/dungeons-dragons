const { description } = require('../../package')

module.exports = {
  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#title
   */
  title: 'Dungeons & Dragons',
  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#description
   */
  description: description,
  base: '/dungeons-dragons/',

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
    editLinkText: 'Aidez nous à améliorer cette page',
    lastUpdated: true,
    nav: [
      {
        text: 'Guide du joueur',
        link: '/guide-joueur/',
      },
      {
        text: 'Guide du développeur',
        link: '/guide-dev/',
      },

      // {
      //   text: 'Config',
      //   link: '/config/',
      // },
      // {
      //   text: 'Guide',
      //   link: '/guide/',
      // },
    ],
    sidebar:
      //  [
      //   // voir pour faire une partie avec les écrans (en ajoutant un lien dans le header)
      //   '/presentation.md',
      //   '/config.md',
      //   '/window.md',
      //   '/save_load.md',
      //   '/game.md',
      //   '/shortcuts.md',
      //   '/map_editor.md',
      //   '/online_game.md',
      // ],
      {
        '/presentation/': [
          {
            title: 'Présentation',
            collapsable: false,
            children: ['presentation'],
          },
        ],
        '/config/': [
          {
            title: 'Configuration',
            collapsable: false,
            children: [''],
          },
        ],
        '/guide-joueur/': [
          {
            title: 'Guide du joueur',
            collapsable: false,
            children: [
              '',
              'start-game',
              'menu',
              'create-game',
              'how-play',
              'shortcuts',
            ],
          },
        ],
        '/guide-dev/': [
          {
            title: 'Guide du développeur',
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
