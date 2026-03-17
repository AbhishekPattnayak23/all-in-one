declare global {
  namespace Cypress {
    interface Chainable {
      registerUser(username: string, email: string, password: string): Chainable<void>
    }
  }
}

Cypress.Commands.add('registerUser', (username: string, email: string, password: string) => {
  cy.visit('/register')
  cy.get('[data-cy=username]').type(username)
  cy.get('[data-cy=email]').type(email)
  cy.get('[data-cy=password]').type(password)
  cy.get('[data-cy=confirmPassword]').type(password)
  cy.get('[data-cy=submit]').click()
})
