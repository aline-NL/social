import React from 'react';
import { render as rtlRender, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import App from './App';

// Mock the LoginPage component to avoid rendering the actual login form
jest.mock('./pages/LoginPage', () => ({
  __esModule: true,
  default: () => <div>Login Page Mock</div>,
}));

// Create a custom render function that includes the required providers
const render = (
  ui: React.ReactElement,
  { route = '/', ...renderOptions } = {}
) => {
  const queryClient = new QueryClient();
  
  const Wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[route]}>
        {children}
      </MemoryRouter>
    </QueryClientProvider>
  );

  return rtlRender(ui, { wrapper: Wrapper, ...renderOptions });
};

describe('App', () => {
  it('renders the login page by default', () => {
    // Render the App component with our custom render function
    render(<App />, { route: '/login' });
    
    // Check that the login page is rendered
    expect(screen.getByText('Login Page Mock')).toBeInTheDocument();
  });
});

// This is needed to make TypeScript happy with the global Jest types
export {};
