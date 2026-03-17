describe('User Registration', () => {
  const validUser = {
    username: 'testuser',
    email: 'test@example.com',
    password: 'SecurePass123!'
  }

  const existingUser = {
    username: 'existinguser',
    email: 'existing@example.com',
    password: 'Password123!'
  }

  before(() => {
    cy.intercept('POST', '/api/auth/register').as('registerRequest')
    cy.intercept('POST', '/api/auth/login').as('loginRequest')
  })

  it('should register a new user with valid credentials', () => {
    cy.visit('/register')
    cy.get('[data-cy=username-input]').type(validUser.username)
    cy.get('[data-cy=email-input]').type(validUser.email)
    cy.get('[data-cy=password-input]').type(validUser.password)
    cy.get('[data-cy=register-button]').click()

    cy.wait('@registerRequest').then((interception) => {
      expect(interception.response.statusCode).to.equal(201)
      expect(interception.response.body.token).to.exist
    })
    
    cy.get('[data-cy=success-message]')
      .should('be.visible')
      .should('contain', 'Registration successful')
  })

  it('should show error for existing username', () => {
    cy.visit('/register')
    cy.get('[data-cy=username-input]').type(existingUser.username)
    cy.get('[data-cy=email-input]').type('new@example.com')
    cy.get('[data-cy=password-input]').type('Password123!')
    cy.get('[data-cy=register-button]').click()

    cy.wait('@registerRequest').then((interception) => {
      expect(interception.response.statusCode).to.equal(400)
    })
    
    cy.get('[data-cy=error-message]')
      .should('be.visible')
      .should('contain', 'Username already exists')
  })

  it('should show error for existing email', () => {
    cy.visit('/register')
    cy.get('[data-cy=username-input]').type('newusername')
    cy.get('[data-cy=email-input]').type(existingUser.email)
    cy.get('[data-cy=password-input]').type('Password123!')
    cy.get('[data-cy=register-button]').click()

    cy.wait('@registerRequest').then((interception) => {
      expect(interception.response.statusCode).to.equal(400)
    })
    
    cy.get('[data-cy=error-message]')
      .should('be.visible')
      .should('contain', 'Email already exists')
  })

  it('should show validation errors for invalid inputs', () => {
    cy.visit('/register')
    
    // Empty form submission
    cy.get('[data-cy=register-button]').click()
    
    cy.get('[data-cy=username-error]')
      .should('be.visible')
      .should('contain', 'Username is required')
    
    cy.get('[data-cy=email-error]')
      .should('be.visible')
      .should('contain', 'Email is required')
    
    cy.get('[data-cy=password-error]')
      .should('be.visible')
      .should('contain', 'Password is required')

    // Invalid email
    cy.get('[data-cy=email-input]').type('invalid-email')
    cy.get('[data-cy=email-error]')
      .should('be.visible')
      .should('contain', 'Please enter a valid email')
  })
})
