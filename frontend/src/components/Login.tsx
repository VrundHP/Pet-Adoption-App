import React, { useState } from 'react';
import './Login.css';

const Login: React.FC<{ onLogin: (email: string) => void }> = ({ onLogin }) => {
  const [isRegistering, setIsRegistering] = useState<boolean>(false);
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:5000';

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${backendUrl}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: email, password }),
      });

      const data = await response.json();
      if (response.ok) {
        onLogin(email); // Notify parent component of successful login
        setError('');
      } else {
        setError(data.message || 'Login failed.');
      }
    } catch (err) {
      console.error('Error logging in:', err);
      setError('An error occurred while logging in. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${backendUrl}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: email, password, email }),
      });

      const data = await response.json();
      if (response.ok) {
        alert(data.message || 'Registration successful!');
        setError('');
        setIsRegistering(false); // Switch back to login form
      } else {
        setError(data.message || 'Registration failed.');
      }
    } catch (err) {
      console.error('Error registering:', err);
      setError('An error occurred while registering. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-box">
        <h2>{isRegistering ? 'Register' : 'Login'}</h2>
        <form onSubmit={isRegistering ? handleRegister : handleLogin} className="login-form">
          <div className="input-container">
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="Email"
            />
          </div>
          <div className="input-container">
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Password"
            />
          </div>

          {error && <p className="error">{error}</p>}
          <button type="submit" disabled={loading}>
            {loading ? 'Loading...' : isRegistering ? 'Register' : 'Login'}
          </button>
        </form>

        <div className="toggle-form">
          <p>
            {isRegistering
              ? 'Already have an account?'
              : "Don't have an account?"}{' '}
            <a href="#" onClick={() => setIsRegistering(!isRegistering)}>
              {isRegistering ? 'Login' : 'Register'}
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
