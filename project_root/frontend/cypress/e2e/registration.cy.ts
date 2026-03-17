describe('User Registration E2E Tests', () => {
  beforeEach(() => {
    cy.visit('/register')
  })

  it('registers new user with valid credentials', () => {
    const uniqueSuffix = Date.now()
    cy.get('[data-cy=username]').type(`testuser${uniqueSuffix}`)
    cy.get('[data-cy=email]').type(`test${uniqueSuffix}@example.com`)
    cy.get('[data-cy=password]').type('ValidPass123!')
    cy.get('[data-cy=confirmPassword]').type('ValidPass123!')
    cy.get('[data-cy=submit]').click()
    
    cy.url().should('include', '/dashboard')
    cy.get('[data-cy=success-message]').should('contain', 'Registration successful')
    cy.window().should('have.property', 'localStorage')
      .and(property => {
        expect(property.getItem('token')).to.exist
      })
  })

  it('prevents registration with existing username', () => {
    // First register the user
    const existingUsername = 'existuser123'
    cy.request('POST', 'http://localhost:8000/api/auth/register', {
      username: existingUsername,
      email: 'exist@example.com',
      password: 'TestPass123!'
    })
    
    cy.visit('/register')
    cy.get('[data-cy=username]').type(existingUsername)
    cy.get('[data-cy=email]').type('new@example.com')
    cy.get('[data-cy=password]').type('ValidPass123!')
    cy.get('[data-cy=confirmPassword]').type('ValidPass123!')
    cy.get('[data-cy=submit]').click()
    
    cy.get('[data-cy=error-message]').should('contain', 'username already exists')
  })

  it('prevents registration with existing email', () => {
    const existingEmail = 'existemail@example.com'
    cy.request('POST', 'http://localhost:8000/api/auth/register', {
      username: 'newuser123',
      email: existingEmail,
      password: 'TestPass123!'
    })
    
    cy.visit('/register')
    cy.get('[data-cy=username]').type('completelynew')
    cy.get('[data-cy=email]').type(existingEmail)
    cy.get('[data-cy=password]').type('ValidPass123!')
    cy.get('[data-cy=confirmPassword]').type('ValidPass123!')
    cy.get('[data-cy=submit]').click()
    
    cy.get('[data-cy=error-message]').should('contain', 'email already exists')
  })

  it('validates weak password', () => {
    cy.get('[data-cy=username]').type('weakpassuser')
    cy.get('[data-cy=email]').type('weak@test.com')
    cy.get('[data-cy=password]').type('123')
    cy.get('[data-cy=confirmPassword]').type('123')
    cy.get('[data-cy=submit]').click()
    
    cy.get('[data-cy=password-error]').should('contain', 'password too weak')
  })

  it('requires email format validation', () => {
    cy.get('[data-cy=username]').type('emailtest')
    cy.get('[data-cy=email]').type('invalid-email')
    cy.get('[data-cy=password]').type('ValidPass123!')
    cy.get('[data-cy=confirmPassword]').type('ValidPass123!')
    cy.get('[data-cy=submit]').click()
    
    cy.get('[data-cy=email-error]').should('contain', 'valid email')
  })

  it('requires password confirmation match', () => {
    cy.get('[data-cy=username]').type('confirmtest')
    cy.get('[data-cy=email]').type('confirm@test.com')
    cy.get('[data-cy=password]').type('ValidPass123!')
    cy.get('[data-cy=confirmPassword]').type('DifferentPass123!')
    cy.get('[data-cy=submit]').click()
    
    cy.get('[data-cy=password-match-error]').should('be.visible')
  })
})
