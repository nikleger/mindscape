const pa11y = require('pa11y');
const assert = require('assert');

async function runAccessibilityTest() {
  try {
    // Test homepage
    const homepageResults = await pa11y('http://localhost:3000', {
      standard: 'WCAG2AA',
      includeNotices: true,
      includeWarnings: true,
      chromeLaunchConfig: {
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
      },
    });

    assert.strictEqual(
      homepageResults.issues.length,
      0,
      `Homepage has ${homepageResults.issues.length} accessibility issues`
    );

    // Test mindmap page
    const mindmapResults = await pa11y('http://localhost:3000/mindmap', {
      standard: 'WCAG2AA',
      includeNotices: true,
      includeWarnings: true,
      chromeLaunchConfig: {
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
      },
    });

    assert.strictEqual(
      mindmapResults.issues.length,
      0,
      `Mindmap page has ${mindmapResults.issues.length} accessibility issues`
    );

    // Test node creation form
    const nodeFormResults = await pa11y('http://localhost:3000/mindmap/new-node', {
      standard: 'WCAG2AA',
      includeNotices: true,
      includeWarnings: true,
      chromeLaunchConfig: {
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
      },
    });

    assert.strictEqual(
      nodeFormResults.issues.length,
      0,
      `Node creation form has ${nodeFormResults.issues.length} accessibility issues`
    );

    console.log('All accessibility tests passed!');
  } catch (error) {
    console.error('Accessibility test failed:', error);
    process.exit(1);
  }
}

runAccessibilityTest(); 