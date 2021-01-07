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
        text: 'Guides',
        link: '/guides/',
      },
    ],
    sidebar: {
      '/presentation/': [
        {
          title: 'Présentation',
          collapsable: false,
          children: [''],
        },
      ],
      '/guides/': [
        '',
        {
          title: 'Guide du joueur',
          collapsable: true,
          children: [
            'joueur/',
            'joueur/start-game',
            'joueur/menu',
            'joueur/create-game',
            'joueur/how-play',
            'joueur/online_game',
            'joueur/shortcuts',
          ],
        },
        {
          title: 'Guide du développeur',
          collapsable: true,
          children: [
            'dev/',
            'dev/config',
            'dev/window',
            'dev/versus',
            'dev/managers',
            'dev/map',
            'dev/save_load',
            'dev/shortcuts',
          ],
        },
      ],
    },
  },

  /**
   * Apply plugins，ref：https://v1.vuepress.vuejs.org/zh/plugin/
   */
  plugins: ['@vuepress/plugin-back-to-top', '@vuepress/plugin-medium-zoom'],
}
