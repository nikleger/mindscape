// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Mindscape Documentation',
  tagline: 'Enterprise Mind Mapping Platform',
  favicon: 'img/favicon.svg',

  // Set the production url of your site here
  url: 'http://localhost',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/',

  // GitHub pages deployment config.
  organizationName: 'mindscape',
  projectName: 'mindscape',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'throw',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: '/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Mindscape',
        logo: {
          alt: 'Mindscape Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            to: 'architecture/meta-strategy',
            label: 'Architecture',
            position: 'left',
          },
          {
            to: 'development/guide',
            label: 'Development',
            position: 'left',
          },
          {
            to: 'api/spec',
            label: 'API',
            position: 'left',
          },
          {
            href: 'https://github.com/mindscape/mindscape',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Documentation',
            items: [
              {
                label: 'Architecture',
                to: 'architecture/meta-strategy',
              },
              {
                label: 'Development',
                to: 'development/guide',
              },
              {
                label: 'API',
                to: 'api/spec',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Discord',
                href: 'https://discord.gg/mindscape',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/mindscape',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/mindscape/mindscape',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Mindscape. Built with Docusaurus.`,
      },
    }),
};

module.exports = config; 