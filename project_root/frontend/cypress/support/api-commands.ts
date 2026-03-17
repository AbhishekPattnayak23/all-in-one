declare global {
  namespace Cypress {
    interface Chainable {
      apiRegister(username: string, email: string, password: string): Chainable
    }
  }
}

Cypress.Commands.add('apiRegister', (username: string, email: string, password: string) => {
  return cy.request({
    method: 'POST',
    url: 'http://localhost:8000/api/auth/register',
    body: { username, email, password }
  })
})
