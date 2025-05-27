/// <reference types="@testing-library/jest-dom" />

declare namespace NodeJS {
  interface Global {
    // Add global variables here if needed
  }
}

declare const expect: jest.Expect;
declare const describe: jest.Describe;
declare const it: jest.It;
declare const test: jest.It;
declare const beforeAll: jest.HookFunction;
declare const afterAll: jest.HookFunction;
declare const beforeEach: jest.HookFunction;
declare const afterEach: jest.HookFunction;
declare const jest: typeof import('@jest/globals').jest;
