import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { Login } from './Login';
import { useAuth } from '../../hooks/useAuth';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';


// Mock the useAuth hook
const mockLogin = jest.fn();

jest.mock('../../hooks/useAuth', () => ({
  useAuth: () => ({
    login: mockLogin,
    isAuthenticated: false,
    loading: false,
  }),
}));

// Mock react-hook-form
jest.mock('react-hook-form', () => ({
  ...jest.requireActual('react-hook-form'),
  useForm: () => ({
    register: jest.fn(),
    handleSubmit: (fn: any) => (e: any) => {
      e?.preventDefault?.();
      fn({ email: 'test@example.com', password: 'password123' });
    },
    formState: { errors: {}, isSubmitting: false },
  }),
}));

const renderLogin = () => {
  return render(
    <QueryClientProvider client={new QueryClient()}>
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    </QueryClientProvider>
  );
};

describe('Login', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders login form', () => {
    renderLogin();

    expect(screen.getByLabelText('E-mail')).toBeInTheDocument();
    expect(screen.getByLabelText('Senha')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /entrar/i })).toBeInTheDocument();
  });

  it('submits the form with email and password', async () => {
    renderLogin();

    await act(async () => {
      fireEvent.input(screen.getByLabelText('E-mail'), {
        target: { value: 'test@example.com' },
      });

      fireEvent.input(screen.getByLabelText('Senha'), {
        target: { value: 'password123' },
      });

      fireEvent.submit(screen.getByRole('button', { name: /entrar/i }));
    });

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('test@example.com', 'password123');
    });
  });

  it('shows loading state when logging in', async () => {
    // Mock loading state
    const { rerender } = renderLogin();
    
    // Get the form elements
    const emailInput = screen.getByLabelText('E-mail');
    const passwordInput = screen.getByLabelText('Senha');
    const submitButton = screen.getByRole('button', { name: /entrar/i });
    
    // Fill out the form
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    
    // Mock the login function to delay resolution
    const loginPromise = new Promise(() => {});
    mockLogin.mockImplementationOnce(() => loginPromise);
    
    // Submit the form
    fireEvent.click(submitButton);
    
    // Check that the button is in loading state
    const loadingButton = await screen.findByRole('button', { name: /entrando.../i });
    expect(loadingButton).toBeDisabled();
    
    // Cleanup
    await act(async () => {
      // Resolve the promise to avoid warnings
      await Promise.resolve();
    });
  });

  it('shows error message when login fails', async () => {
    const errorMessage = 'Credenciais inválidas';
    
    // Mock the login function to reject with an error
    mockLogin.mockRejectedValueOnce(new Error(errorMessage));

    renderLogin();

    // Fill out the form
    await act(async () => {
      const emailInput = screen.getByLabelText('E-mail');
      const passwordInput = screen.getByLabelText('Senha');
      const submitButton = screen.getByRole('button', { name: /entrar/i });

      fireEvent.change(emailInput, { target: { value: 'wrong@example.com' } });
      fireEvent.change(passwordInput, { target: { value: 'wrongpassword' } });
      fireEvent.click(submitButton);
    });

    // Wait for the error message to appear
    const errorElement = await screen.findByText(/erro ao fazer login/i, { exact: false });
    expect(errorElement).toBeInTheDocument();
  });
});
