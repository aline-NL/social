// Mock next/dynamic to avoid async components in tests
jest.mock('next/dynamic', () => (dynamicImport: any) => {
  const DynamicComponent = ({ children, ...props }: any) => {
    const Component = dynamicImport();
    return <Component {...props}>{children}</Component>;
  };
  return DynamicComponent;
});

// Mock window.matchMedia which is not implemented in JSDOM
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock window.scrollTo
window.scrollTo = jest.fn();

// Mock ResizeObserver
class ResizeObserverMock {
  observe() {}
  unobserve() {}
  disconnect() {}
}

window.ResizeObserver = ResizeObserverMock;

export {};
