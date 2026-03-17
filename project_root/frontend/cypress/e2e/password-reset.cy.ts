describe('Password Reset Flow', () => {
  const testUser = {
    email: 'test@example.com',
    password: 'TestPass123!',
    username: 'testuser'
  }

  beforeEach(() => {
    cy.visit('http://localhost:5173')
  })

  it('should complete password reset flow successfully', () => {
    // Navigate to password reset
    cy.get('[data-cy=login-link]').click()
    cy.get('[data-cy=forgot-password-link]').click()
    
    // Request reset
    cy.get('[data-cy=reset-email-input]').type(testUser.email)
    cy.get('[data-cy=reset-submit]').click()
    
    cy.get('[data-cy=reset-message]').should('contain', 'Reset email sent')
    
    // Get reset token from email (simulated for console backend)
    cy.window().then(win => {
      const emailContent = win.console.messages?.find(m => m.includes('reset')) || 'token=abc123'
      const token = emailContent.match(/token=([a-zA-Z0-9-]+)/)?.[1] || 'abc123'
      
      // Click reset link
      cy.visit(`http://localhost:5173/reset-password/${token}`)
      
      // Enter new password
      cy.get('[data-cy=new-password-input]').type('NewPass456!')
      cy.get('[data-cy=confirm-password-input]').type('NewPass456!')
      cy.get('[data-cy=confirm-reset]').click()
      
      cy.get('[data-cy=reset-success]').should('be.visible')
    })
  })
})
