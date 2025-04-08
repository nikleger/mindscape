import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '0bf'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '7e7'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', '726'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', '102'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', 'd76'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '51c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/',
    component: ComponentCreator('/', '989'),
    routes: [
      {
        path: '/',
        component: ComponentCreator('/', 'b09'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/api/spec',
        component: ComponentCreator('/api/spec', 'fa6'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/architecture/core-strategy',
        component: ComponentCreator('/architecture/core-strategy', '09f'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/architecture/meta-strategy',
        component: ComponentCreator('/architecture/meta-strategy', '203'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/database/schema',
        component: ComponentCreator('/database/schema', '2b8'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/development/development-strategy',
        component: ComponentCreator('/development/development-strategy', 'c1b'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/development/guide',
        component: ComponentCreator('/development/guide', 'b7d'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/DOCUMENTATION_INDEX',
        component: ComponentCreator('/DOCUMENTATION_INDEX', 'f06'),
        exact: true
      },
      {
        path: '/infrastructure/overview',
        component: ComponentCreator('/infrastructure/overview', '532'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/intro',
        component: ComponentCreator('/intro', 'f92'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/operations/infrastructure-strategy',
        component: ComponentCreator('/operations/infrastructure-strategy', 'ebe'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/operations/monitoring-strategy',
        component: ComponentCreator('/operations/monitoring-strategy', '3f6'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/process/documentation-strategy',
        component: ComponentCreator('/process/documentation-strategy', 'b17'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/process/infrastructure-implementation',
        component: ComponentCreator('/process/infrastructure-implementation', '9ac'),
        exact: true
      },
      {
        path: '/process/sprint-zero-planning',
        component: ComponentCreator('/process/sprint-zero-planning', 'ab2'),
        exact: true
      },
      {
        path: '/process/sprint-zero-review',
        component: ComponentCreator('/process/sprint-zero-review', 'e27'),
        exact: true
      },
      {
        path: '/process/team-strategy',
        component: ComponentCreator('/process/team-strategy', '1e1'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/process/troubleshooting-audit',
        component: ComponentCreator('/process/troubleshooting-audit', 'd1c'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/quality/quality-strategy',
        component: ComponentCreator('/quality/quality-strategy', 'e01'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/security/security-strategy',
        component: ComponentCreator('/security/security-strategy', '168'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/strategy/',
        component: ComponentCreator('/strategy/', '295'),
        exact: true
      },
      {
        path: '/test-dashboard',
        component: ComponentCreator('/test-dashboard', '633'),
        exact: true,
        sidebar: "docs"
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
