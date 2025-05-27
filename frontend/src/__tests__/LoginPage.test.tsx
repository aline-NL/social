import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { LoginPage } from '../pages/LoginPage';

// Mock the useAuth hook
const mockLogin = jest.fn();
const mockLogout = jest.fn();

jest.mock('../context/AuthContext', () => ({
  useAuth: () => ({
    login: mockLogin,
    user: null,
    logout: mockLogout,
  }),
}));

// Mock the useLocation and useNavigate hooks
const mockUseLocation = jest.fn();
const mockUseNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useLocation: () => mockUseLocation(),
  useNavigate: () => mockUseNavigate,
}));

// Create a test wrapper with required providers
const TestWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const queryClient = new QueryClient();
  
  return (
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>
        {children}
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('LoginPage', () => {
  beforeEach(() => {
    // Reset all mocks before each test
    jest.clearAllMocks();
    
    // Setup default mocks
    mockUseLocation.mockReturnValue({
      pathname: '/login',
      search: '',
      state: { from: { pathname: '/' } },
      key: 'test-key',
      hash: '',
    });
    
    // Mock successful login by default
    mockLogin.mockResolvedValue({});
  });

  it('renders the login page with email and password fields', () => {
    render(
      <TestWrapper>
        <LoginPage />
      </TestWrapper>
    );
    
    // Check that the login page is rendered with the correct title
    expect(screen.getByText('Acesse sua conta')).toBeInTheDocument();
    
    // Check that the email and password fields are rendered
    expect(screen.getByPlaceholderText('E-mail')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Senha')).toBeInTheDocument();
    
    // Check that the login button is rendered
    expect(screen.getByRole('button', { name: /entrar/i })).toBeInTheDocument();
  });
  
  it('shows validation errors when form is submitted with empty fields', async () => {
    // Mock console.error to avoid seeing expected error logs in test output
    const originalError = console.error;
    console.error = jest.fn();
    
    // Mock the login function
    mockLogin.mockImplementation(() => Promise.resolve({}));
    
    render(
      <TestWrapper>
        <LoginPage />
      </TestWrapper>
    );
    
    // Debug: Log the current state of the rendered component
    screen.debug();
    
    // Find the form and submit it directly
    const form = screen.getByTestId('login-form');
    const formSubmit = jest.fn(e => e.preventDefault());
    form.onsubmit = formSubmit;
    
    // Submit the form
    fireEvent.submit(form);
    
    // Debug: Log the form submission
    console.log('Form submitted');
    
    // Check if the form submission was prevented (which it should be by default)
    expect(formSubmit).toHaveBeenCalledTimes(1);
    
    // Check for the error message directly in the document
    const errorElement = screen.queryByText('Por favor, preencha todos os campos');
    console.log('Error element:', errorElement);
    
    // If the error message is not found, log the document body for debugging
    if (!errorElement) {
      console.log('Document body:', document.body.innerHTML);
    }
    
    // Check that login was not called
    expect(mockLogin).not.toHaveBeenCalled();
    
    // Restore console.error
    console.error = originalError;
    
    // Check that the error message is in the document
    expect(errorElement).toBeInTheDocument();
  });
  
  it('calls login with email and password when form is submitted', async () => {
    const user = userEvent.setup();
    const testEmail = 'test@example.com';
    const testPassword = 'password123';
    
    render(
      <TestWrapper>
        <LoginPage />
      </TestWrapper>
    );
    
    // Fill in the form
    const emailInput = screen.getByPlaceholderText('E-mail');
    const passwordInput = screen.getByPlaceholderText('Senha');
    
    await user.type(emailInput, testEmail);
    await user.type(passwordInput, testPassword);
    
    // Submit the form
    const submitButton = screen.getByRole('button', { name: /entrar/i });
    await user.click(submitButton);
    
    // Check that login was called with the correct credentials
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith(testEmail, testPassword);
    });
  });
  
  it('navigates to the home page after successful login', async () => {
    const user = userEvent.setup();
    // Mock a successful login
    mockLogin.mockResolvedValueOnce({});
    
    render(
      <TestWrapper>
        <LoginPage />
      </TestWrapper>
    );
    
    // Fill in the form
    const emailInput = screen.getByPlaceholderText('E-mail');
    const passwordInput = screen.getByPlaceholderText('Senha');
    
    await user.type(emailInput, 'test@example.com');
    await user.type(passwordInput, 'password123');
    
    // Submit the form
    const submitButton = screen.getByRole('button', { name: /entrar/i });
    await user.click(submitButton);
    
    // Check that navigation occurred after successful login
    await waitFor(() => {
      expect(mockUseNavigate).toHaveBeenCalledWith('/', { replace: true });
    });
  });
  
  it('shows an error message when login fails', async () => {
    const user = userEvent.setup();
    // Mock a failed login
    const errorMessage = 'Credenciais inválidas';
    mockLogin.mockRejectedValueOnce(new Error(errorMessage));
    
    render(
      <TestWrapper>
        <LoginPage />
      </TestWrapper>
    );
    
    // Fill in the form
    const emailInput = screen.getByPlaceholderText('E-mail');
    const passwordInput = screen.getByPlaceholderText('Senha');
    
    await user.type(emailInput, 'wrong@example.com');
    await user.type(passwordInput, 'wrongpassword');
    
    // Submit the form
    const submitButton = screen.getByRole('button', { name: /entrar/i });
    await user.click(submitButton);
    
    // Check that the error message is displayed
    expect(await screen.findByText(/credenciais inválidas/i)).toBeInTheDocument();
  });
});

export {};
