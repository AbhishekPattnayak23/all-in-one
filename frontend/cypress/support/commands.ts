/// <reference types="cypress" />

interface UserFixture {
  username: string;
  password: string;
}

declare global {
  namespace Cypress {
    interface Chainable {
      /**
       * Log in via API, stores JWT token & redirects to dashboard.
       * Relies on fixture "user.json" unless partial fixture provided.
       */
      login(user?: Partial<UserFixture>): Chainable<void>;
    }
  }
}

Cypress.Commands.add('login', (user) => {
  const fallbackUser: UserFixture = {
    username: 'testuser',
    password: 'Str0ngP@ss!',
  };
  const payload = { ...fallbackUser, ...user };
  cy.session(
    JSON.stringify(payload),
    () => {
      cy.request({
        method: 'POST',
        url: 'http://frontend:3000/api/auth/login',
        body: { username: payload.username, password: payload.password },
      }).then(({ body }) => {
        cy.visit('/', {
          onBeforeLoad(win) {
            win.localStorage.setItem('token', body.token);
          },
        });
      });
    },
    {
      validate() {
        cy.request({
          method: 'GET',
          url: 'http://frontend:3000/api/user/me',
          headers: {
            Authorization: `Bearer ${window.localStorage.getItem('token')}`,
          },
        });
      },
    }
  );
  cy.visit('/dashboard');
});
