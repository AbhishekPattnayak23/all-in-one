import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://frontend:3000',
    supportFile: 'cypress/support/e2e.ts',
  },
});
