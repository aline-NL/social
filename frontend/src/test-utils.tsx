import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, RenderOptions } from '@testing-library/react';
import React, { ReactElement, ReactNode, useState, createContext } from 'react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { ThemeContext as OriginalThemeContext } from './context/ThemeContext';
import { AuthContext } from './context/AuthContext';
import { User, UserRole } from './types';

// Create a test ThemeContext
const ThemeContext = createContext({
  theme: 'light',
  toggleTheme: () => {},
});

// Re-export the ThemeContext type
type ThemeContextType = React.ContextType<typeof ThemeContext>;

// Extend the AuthContext type for testing
type TestAuthContextType = React.ContextType<typeof AuthContext>;

// Create a test ThemeProvider component
const TestThemeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [theme, setTheme] = React.useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    setTheme(prevTheme => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  const themeContextValue: ThemeContextType = {
    theme,
    toggleTheme,
  };

  return (
    <ThemeContext.Provider value={themeContextValue}>
      {children}
    </ThemeContext.Provider>
  );
};

// Create a test AuthProvider component that implements the AuthContextType
const TestAuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const mockUser: User = {
    id: 1,
    email: 'test@example.com',
    first_name: 'Test',
    last_name: 'User',
    tipo: 'admin' as UserRole,
    is_active: true,
    date_joined: new Date().toISOString(),
  };

  const login = async (_email: string, _password: string) => {
    // Mock login implementation
    return Promise.resolve();
  };

  const logout = () => {
    // Mock logout implementation
    return Promise.resolve();
  };

  const contextValue: TestAuthContextType = {
    user: mockUser,
    loading: false,
    login,
    logout,
    isAuthenticated: true,
    isAdmin: mockUser.tipo === 'admin',
    isAttendant: mockUser.tipo === 'atendente',
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

type CustomRenderOptions = Omit<RenderOptions, 'wrapper'> & {
  route?: string;
  path?: string;
};

// Use the test providers
const AuthProvider = TestAuthProvider;
const ThemeProviderWrapper = TestThemeProvider;

// Create a simplified AuthProvider that doesn't use Router
const TestAuthProviderWrapper: React.FC<{ children: ReactNode }> = ({ children }) => {
  const mockUser: User = {
    id: 1,
    email: 'test@example.com',
    first_name: 'Test',
    last_name: 'User',
    tipo: 'admin',
    is_active: true,
    date_joined: new Date().toISOString(),
  };

  const login = async (_email: string, _password: string) => {
    return Promise.resolve();
  };

  const logout = () => {
    return Promise.resolve();
  };

  return (
    <AuthContext.Provider
      value={{
        user: mockUser,
        loading: false,
        login,
        logout,
        isAuthenticated: true,
        isAdmin: mockUser.tipo === 'admin',
        isAttendant: mockUser.tipo === 'atendente',
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

const AllTheProviders = ({ children }: { children: ReactNode }) => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProviderWrapper>
        <MemoryRouter>
          <TestAuthProviderWrapper>
            {children}
          </TestAuthProviderWrapper>
        </MemoryRouter>
      </ThemeProviderWrapper>
    </QueryClientProvider>
  );
};

const customRender = (
  ui: ReactElement,
  { route = '/', path = '*', ...options }: CustomRenderOptions = {}
) => {
  window.history.pushState({}, 'Test page', route);
  
  return render(
    <AllTheProviders>
      <Routes>
        <Route path={path} element={ui} />
      </Routes>
    </AllTheProviders>,
    options
  );
};

export * from '@testing-library/react';
export { customRender as render };
