import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MockedProvider } from '@apollo/client/testing';
import { Auth } from '../../components/Auth';
import { LOGIN_MUTATION, REGISTER_MUTATION, RESET_PASSWORD_MUTATION } from '../../graphql/mutations';

// Mock next/router
jest.mock('next/router', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

describe('Auth Component', () => {
  const mockLoginSuccess = {
    request: {
      query: LOGIN_MUTATION,
      variables: {
        email: 'test@example.com',
        password: 'password123',
      },
    },
    result: {
      data: {
        login: {
          token: 'mock-token',
          user: {
            id: '1',
            email: 'test@example.com',
            fullName: 'Test User',
          },
        },
      },
    },
  };

  const mockRegisterSuccess = {
    request: {
      query: REGISTER_MUTATION,
      variables: {
        email: 'test@example.com',
        password: 'password123',
        fullName: 'Test User',
      },
    },
    result: {
      data: {
        register: {
          token: 'mock-token',
          user: {
            id: '1',
            email: 'test@example.com',
            fullName: 'Test User',
          },
        },
      },
    },
  };

  const mockResetPasswordSuccess = {
    request: {
      query: RESET_PASSWORD_MUTATION,
      variables: {
        email: 'test@example.com',
        newPassword: 'newpassword123',
      },
    },
    result: {
      data: {
        resetPassword: {
          success: true,
          message: 'Password reset successful',
        },
      },
    },
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders login form by default', () => {
    render(
      <MockedProvider mocks={[]} addTypename={false}>
        <Auth />
      </MockedProvider>
    );

    expect(screen.getByText('Login')).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByText('Continue with Google')).toBeInTheDocument();
    expect(screen.getByText('Continue with GitHub')).toBeInTheDocument();
  });

  it('switches to register form', () => {
    render(
      <MockedProvider mocks={[]} addTypename={false}>
        <Auth />
      </MockedProvider>
    );

    fireEvent.click(screen.getByText('Create an account'));
    expect(screen.getByText('Register')).toBeInTheDocument();
    expect(screen.getByLabelText('Full Name')).toBeInTheDocument();
  });

  it('handles login form submission', async () => {
    render(
      <MockedProvider mocks={[mockLoginSuccess]} addTypename={false}>
        <Auth />
      </MockedProvider>
    );

    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' },
    });
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'password123' },
    });
    fireEvent.click(screen.getByText('Login'));

    await waitFor(() => {
      expect(localStorageMock.setItem).toHaveBeenCalledWith('token', 'mock-token');
    });
  });

  it('handles register form submission', async () => {
    render(
      <MockedProvider mocks={[mockRegisterSuccess]} addTypename={false}>
        <Auth />
      </MockedProvider>
    );

    fireEvent.click(screen.getByText('Create an account'));
    fireEvent.change(screen.getByLabelText('Full Name'), {
      target: { value: 'Test User' },
    });
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' },
    });
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'password123' },
    });
    fireEvent.click(screen.getByText('Register'));

    await waitFor(() => {
      expect(localStorageMock.setItem).toHaveBeenCalledWith('token', 'mock-token');
    });
  });

  it('shows validation errors', async () => {
    render(
      <MockedProvider mocks={[]} addTypename={false}>
        <Auth />
      </MockedProvider>
    );

    fireEvent.click(screen.getByText('Login'));
    expect(screen.getByText('Email is required')).toBeInTheDocument();
    expect(screen.getByText('Password is required')).toBeInTheDocument();
  });

  it('handles social login', async () => {
    render(
      <MockedProvider mocks={[]} addTypename={false}>
        <Auth />
      </MockedProvider>
    );

    fireEvent.click(screen.getByText('Continue with Google'));
    // Add social login specific tests here
  });

  it('handles forgot password flow', async () => {
    render(
      <MockedProvider mocks={[mockResetPasswordSuccess]} addTypename={false}>
        <Auth />
      </MockedProvider>
    );

    fireEvent.click(screen.getByText('Forgot password?'));
    expect(screen.getByText('Reset Password')).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' },
    });
    fireEvent.change(screen.getByLabelText('New Password'), {
      target: { value: 'newpassword123' },
    });
    fireEvent.change(screen.getByLabelText('Confirm Password'), {
      target: { value: 'newpassword123' },
    });
    fireEvent.click(screen.getByText('Reset Password'));

    await waitFor(() => {
      expect(screen.getByText('Login')).toBeInTheDocument();
    });
  });

  it('handles remember me functionality', () => {
    render(
      <MockedProvider mocks={[]} addTypename={false}>
        <Auth />
      </MockedProvider>
    );

    const rememberMeCheckbox = screen.getByLabelText('Remember me');
    expect(rememberMeCheckbox).toBeInTheDocument();
    fireEvent.click(rememberMeCheckbox);
    expect(rememberMeCheckbox).toBeChecked();
  });

  it('handles error messages', async () => {
    const mockLoginError = {
      request: {
        query: LOGIN_MUTATION,
        variables: {
          email: 'test@example.com',
          password: 'wrongpassword',
        },
      },
      error: new Error('Invalid credentials'),
    };

    render(
      <MockedProvider mocks={[mockLoginError]} addTypename={false}>
        <Auth />
      </MockedProvider>
    );

    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' },
    });
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'wrongpassword' },
    });
    fireEvent.click(screen.getByText('Login'));

    await waitFor(() => {
      expect(screen.getByText('Invalid credentials')).toBeInTheDocument();
    });
  });
}); 