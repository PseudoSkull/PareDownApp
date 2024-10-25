// ./components/LoginForm.jsx
import React, { useState } from 'react';

const LoginForm = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [attempts, setAttempts] = useState(0);
  const [lockedOut, setLockedOut] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (lockedOut) return;

    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        setError(null);
        onLoginSuccess();
      } else {
        setAttempts((prev) => prev + 1);
        setError('Username or password was incorrect');
        if (attempts >= 4) {
          setLockedOut(true);
          setTimeout(() => {
            setLockedOut(false);
            setAttempts(0);
          }, 180000); // 3 minutes
        }
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      {lockedOut && <p>You have been locked out for 3 minutes due to too many failed attempts.</p>}
      {error && <p>{error}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </label>
        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        <button type="submit" disabled={lockedOut}>Log In</button>
      </form>
    </div>
  );
};

export default LoginForm;
