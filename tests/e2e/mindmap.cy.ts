describe('Mindmap E2E Tests', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.login('test@example.com', 'password');
  });

  it('creates a new mindmap', () => {
    cy.get('[data-testid="create-mindmap-button"]').click();
    cy.get('[data-testid="mindmap-title-input"]').type('Test Mindmap');
    cy.get('[data-testid="save-mindmap-button"]').click();
    cy.contains('Test Mindmap').should('be.visible');
  });

  it('adds nodes to mindmap', () => {
    cy.createMindmap('Test Mindmap');
    cy.get('[data-testid="add-node-button"]').click();
    cy.get('[data-testid="node-content-input"]').type('Test Node');
    cy.get('[data-testid="save-node-button"]').click();
    cy.contains('Test Node').should('be.visible');
  });

  it('connects nodes', () => {
    cy.createMindmap('Test Mindmap');
    cy.addNode('First Node');
    cy.addNode('Second Node');
    cy.get('[data-testid="connect-nodes-button"]').click();
    cy.get('[data-testid="first-node"]').click();
    cy.get('[data-testid="second-node"]').click();
    cy.get('[data-testid="connection"]').should('be.visible');
  });

  it('saves mindmap changes', () => {
    cy.createMindmap('Test Mindmap');
    cy.addNode('Test Node');
    cy.get('[data-testid="save-mindmap-button"]').click();
    cy.reload();
    cy.contains('Test Node').should('be.visible');
  });
}); 