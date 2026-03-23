import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: [],
    include: ['tests/**/*.test.js'],
    exclude: ['node_modules', 'dist', '.idea', '.git', '.cache'],
    reporters: ['verbose'],
    testTimeout: 10000,
  },
});
