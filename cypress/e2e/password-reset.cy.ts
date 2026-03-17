describe('Password Reset Flow', () => {
  const testEmail = 'test@example.com';
  const newPassword = 'NewSecurePass123!';

  beforeEach(() => {
    cy.visit('http://localhost:5173');
  });

  it('should request password reset via email', () => {
    cy.get('[data-testid="forgot-password-link"]').click();
    cy.url().should('include', '/forgot-password');
    
    cy.get('[data-testid="email-input"]').type(testEmail);
    cy.get('[data-testid="submit-reset-request"]').click();
    
    cy.get('[data-testid="success-message"]')
      .should('contain', 'Password reset email sent');
  });

  it('should confirm password reset with valid token', () => {
    const validToken = 'test-token-123';
    cy.visit(`http://localhost:5173/reset-password/${validToken}`);
    
    cy.get('[data-testid="new-password-input"]').type(newPassword);
    cy.get('[data-testid="confirm-password-input"]').type(newPassword);
    cy.get('[data-testid="submit-password-reset"]').click();
    
    cy.get('[data-testid="success-message"]')
      .should('contain', 'Password reset successful');
    cy.url().should('include', '/login');
  });

  it('should handle expired/invalid token', () => {
    const invalidToken = 'invalid-token';
    cy.visit(`http://localhost:5173/reset-password/${invalidToken}`);
    
    cy.get('[data-testid="new-password-input"]').type(newPassword);
    cy.get('[data-testid="submit-password-reset"]').click();
    
    cy.get('[data-testid="error-message"]')
      .should('contain', 'Invalid or expired token');
  });
});
