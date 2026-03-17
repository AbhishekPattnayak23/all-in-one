describe('UserLogin', () => {
  const INVALID_CREDS = { username: 'baduser', password: 'badpass' };

  beforeEach(() => 'logout');

  it('happy path -- logs in & redirects to dashboard', () => {
    cy.visit('/login');
    cy.intercept('POST', '/api/auth/login').as('loginReq');

    cy.fixture('user.json').then((user) => {
      cy.get('input[name="username"]').type(user.username);
      cy.get('input[name="password"]').type(user.password);
    });
    cy.get('button[type="submit"]').click();

    cy.wait('@loginReq').its('response.statusCode').should('eq', 200);
    cy.url().should('include', '/dashboard');
    cy.window()
      .its('localStorage.token')
      .should('be.a', 'string');
  });

  it('error flow -- invalid credentials shows banner, remains on login', () => {
    cy.visit('/login');
    cy.intercept('POST', '/api/auth/login').as('loginReq');

    cy.get('input[name="username"]').type(INVALID_CREDS.username);
    cy.get('input[name="password"]').type(INVALID_CREDS.password);
    cy.get('button[type="submit"]').click();

    cy.wait('@loginReq').then((xhr) => {
      expect(xhr.response?.statusCode).to.eq(400);
      expect(xhr.response?.body).to.have.property('error_code', 'invalid_credentials');
      cy.contains(xhr.response?.body.detail).should('be.visible');
    });

    cy.url().should('include', '/login');
  });
});
