import React, { useState } from 'react';
import { useRouter } from 'next/router';
import { useMutation } from '@apollo/client';
import { LOGIN_MUTATION, REGISTER_MUTATION, RESET_PASSWORD_MUTATION } from '../graphql/mutations';

interface AuthProps {
  initialMode?: 'login' | 'register' | 'reset';
}

export const Auth: React.FC<AuthProps> = ({ initialMode = 'login' }) => {
  const router = useRouter();
  const [mode, setMode] = useState<'login' | 'register' | 'reset'>(initialMode);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    fullName: '',
    newPassword: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const [login] = useMutation(LOGIN_MUTATION);
  const [register] = useMutation(REGISTER_MUTATION);
  const [resetPassword] = useMutation(RESET_PASSWORD_MUTATION);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setErrors(prev => ({ ...prev, [name]: '' }));
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    
    if (!formData.email) {
      newErrors.email = 'Email is required';
    }
    
    if (mode === 'login' || mode === 'register') {
      if (!formData.password) {
        newErrors.password = 'Password is required';
      }
    }
    
    if (mode === 'register') {
      if (!formData.fullName) {
        newErrors.fullName = 'Full name is required';
      }
    }
    
    if (mode === 'reset') {
      if (!formData.newPassword) {
        newErrors.newPassword = 'New password is required';
      }
      if (!formData.confirmPassword) {
        newErrors.confirmPassword = 'Please confirm your password';
      }
      if (formData.newPassword !== formData.confirmPassword) {
        newErrors.confirmPassword = 'Passwords do not match';
      }
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      if (mode === 'login') {
        const { data } = await login({
          variables: {
            email: formData.email,
            password: formData.password,
          },
        });
        localStorage.setItem('token', data.login.token);
        router.push('/dashboard');
      } else if (mode === 'register') {
        const { data } = await register({
          variables: {
            email: formData.email,
            password: formData.password,
            fullName: formData.fullName,
          },
        });
        localStorage.setItem('token', data.register.token);
        router.push('/dashboard');
      } else if (mode === 'reset') {
        await resetPassword({
          variables: {
            email: formData.email,
            newPassword: formData.newPassword,
          },
        });
        setMode('login');
      }
    } catch (error) {
      setErrors({ submit: 'Invalid credentials' });
    }
  };

  const handleSocialLogin = async (provider: 'google' | 'github') => {
    // Implement social login logic here
    router.push('/dashboard');
  };

  return (
    <div className="auth-container">
      <h1>{mode === 'login' ? 'Login' : mode === 'register' ? 'Register' : 'Reset Password'}</h1>
      
      <form onSubmit={handleSubmit}>
        {mode === 'register' && (
          <div className="form-group">
            <label htmlFor="fullName">Full Name</label>
            <input
              type="text"
              id="fullName"
              name="fullName"
              value={formData.fullName}
              onChange={handleChange}
            />
            {errors.fullName && <span className="error">{errors.fullName}</span>}
          </div>
        )}

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
          {errors.email && <span className="error">{errors.email}</span>}
        </div>

        {mode !== 'reset' && (
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
            />
            {errors.password && <span className="error">{errors.password}</span>}
          </div>
        )}

        {mode === 'reset' && (
          <>
            <div className="form-group">
              <label htmlFor="newPassword">New Password</label>
              <input
                type="password"
                id="newPassword"
                name="newPassword"
                value={formData.newPassword}
                onChange={handleChange}
              />
              {errors.newPassword && <span className="error">{errors.newPassword}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
              />
              {errors.confirmPassword && <span className="error">{errors.confirmPassword}</span>}
            </div>
          </>
        )}

        {mode === 'login' && (
          <div className="form-group">
            <label>
              <input type="checkbox" name="rememberMe" />
              Remember me
            </label>
          </div>
        )}

        {errors.submit && <div className="error">{errors.submit}</div>}

        <button type="submit">
          {mode === 'login' ? 'Login' : mode === 'register' ? 'Register' : 'Reset Password'}
        </button>
      </form>

      {mode === 'login' && (
        <>
          <button onClick={() => handleSocialLogin('google')}>
            Continue with Google
          </button>
          <button onClick={() => handleSocialLogin('github')}>
            Continue with GitHub
          </button>
          <p>
            Don't have an account?{' '}
            <button onClick={() => setMode('register')}>Create an account</button>
          </p>
          <p>
            <button onClick={() => setMode('reset')}>Forgot password?</button>
          </p>
        </>
      )}

      {mode === 'register' && (
        <p>
          Already have an account?{' '}
          <button onClick={() => setMode('login')}>Login</button>
        </p>
      )}

      {mode === 'reset' && (
        <p>
          Remember your password?{' '}
          <button onClick={() => setMode('login')}>Login</button>
        </p>
      )}
    </div>
  );
}; 