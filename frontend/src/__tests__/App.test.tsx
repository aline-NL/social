import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from '../App';

// Mock the LoginPage component to avoid rendering the actual login form
jest.mock('../pages/LoginPage', () => ({
  __esModule: true,
  default: () => <div>Login Page Mock</div>,
}));

// Create a test-utils file to avoid duplicating this setup
const TestWrapper: React.FC<{ children: React.ReactNode; route?: string }> = ({
  children,
  route = '/',
}) => {
  const queryClient = new QueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[route]}>
        {children}
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('App', () => {
  it('renders the login page by default', () => {
    // Render only the App component without its own router
    render(
      <TestWrapper route="/login">
        <App />
      </TestWrapper>
    );
    
    // Check that the login page is rendered
    expect(screen.getByText('Login Page Mock')).toBeInTheDocument();
  });
});

export {};
