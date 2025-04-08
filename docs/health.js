const express = require('express');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const app = express();
const port = 3001;

// Health check endpoint
app.get('/health', async (req, res) => {
  try {
    const healthStatus = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      checks: {
        server: true,
        documentation: await checkDocumentation(),
        build: await checkBuildProcess(),
        links: await checkLinks()
      }
    };

    res.json(healthStatus);
  } catch (error) {
    res.status(500).json({
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      error: error.message
    });
  }
});

// Check documentation files
async function checkDocumentation() {
  const requiredFiles = [
    'docs/index.md',
    'docs/intro.md',
    'docs/test-dashboard.md',
    'docs/architecture/core-strategy.md',
    'docs/architecture/meta-strategy.md',
    'docs/development/development-strategy.md',
    'docs/development/guide.md',
    'docs/operations/infrastructure-strategy.md',
    'docs/operations/monitoring-strategy.md',
    'docs/process/documentation-strategy.md',
    'docs/process/team-strategy.md',
    'docs/process/troubleshooting-audit.md',
    'docs/quality/quality-strategy.md',
    'docs/security/security-strategy.md'
  ];

  const missingFiles = [];
  for (const file of requiredFiles) {
    if (!fs.existsSync(path.join(__dirname, file))) {
      missingFiles.push(file);
    }
  }

  return {
    status: missingFiles.length === 0,
    missingFiles
  };
}

// Check build process
async function checkBuildProcess() {
  return new Promise((resolve) => {
    exec('npm run build', { cwd: __dirname }, (error) => {
      resolve({
        status: !error,
        error: error ? error.message : null
      });
    });
  });
}

// Check links
async function checkLinks() {
  const linkChecker = require('link-checker');
  const brokenLinks = [];

  // Add link checking logic here
  // This is a placeholder for the actual implementation

  return {
    status: brokenLinks.length === 0,
    brokenLinks
  };
}

// Start the server
app.listen(port, () => {
  console.log(`Health check server running on port ${port}`);
}); 