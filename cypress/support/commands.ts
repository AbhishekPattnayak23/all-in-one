/// <reference types="cypress" />

declare global {
  namespace Cypress {
    interface Chainable {
      register(user: {
        username: string;
        email: string;
        password: string;
      }): Chainable<Response>;
      login(username: string, password: string): Chainable<void>;
    }
  }
}

Cypress.Commands.add('register', (user) => {
  return cy.request('POST', 'http://localhost:8000/api/auth/register', {
    username: user.username,
    email: user.email,
    password: user.password
  })
})

Cypress.Commands.add('login', (username: string, password: string) => {
  cy.visit('/login')
  cy.get('input[name="username"]').type(username)
  cy.get('input[name="password"]').type(password)
  cy.get('button[type="submit"]').click()
  cy.url().should('include', '/dashboard')
})
