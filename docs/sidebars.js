// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docs: [
    'index',
    'intro',
    'test-dashboard',
    {
      type: 'category',
      label: 'Architecture',
      items: [
        'architecture/core-strategy',
        'architecture/meta-strategy',
      ],
    },
    {
      type: 'category',
      label: 'Development',
      items: [
        'development/development-strategy',
        'development/guide',
      ],
    },
    {
      type: 'category',
      label: 'Operations',
      items: [
        'operations/infrastructure-strategy',
        'operations/monitoring-strategy',
      ],
    },
    {
      type: 'category',
      label: 'Process',
      items: [
        'process/documentation-strategy',
        'process/team-strategy',
        'process/troubleshooting-audit',
      ],
    },
    {
      type: 'category',
      label: 'Quality',
      items: [
        'quality/quality-strategy',
      ],
    },
    {
      type: 'category',
      label: 'Security',
      items: [
        'security/security-strategy',
      ],
    },
    {
      type: 'category',
      label: 'Technical Documentation',
      items: [
        'api/spec',
        'database/schema',
        'infrastructure/overview',
      ],
    },
  ],
};

module.exports = sidebars;
