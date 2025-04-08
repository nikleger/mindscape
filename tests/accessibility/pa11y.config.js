module.exports = {
  defaults: {
    standard: 'WCAG2AA',
    timeout: 30000,
    chromeLaunchConfig: {
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    },
  },
  urls: [
    'http://localhost:3000',
    'http://localhost:3000/login',
    'http://localhost:3000/dashboard',
  ],
  reporters: ['cli', 'html'],
  html: {
    output: 'reports/accessibility.html',
  },
  screenCapture: {
    path: 'reports/screenshots',
  },
}; 