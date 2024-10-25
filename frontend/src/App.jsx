// ./App.jsx
import { useState, useEffect } from 'react';
import './App.css';
import DataForm from './components/TestItemForm';
import LoginForm from './components/LoginForm';

function App() {

  // Check localStorage to see if the user is authenticated
  const [isAuthenticated, setIsAuthenticated] = useState(
    localStorage.getItem('isAuthenticated')
  );

  // Handle successful login by updating state and storing in localStorage
  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
    localStorage.setItem('isAuthenticated', 'true'); // Save authentication status in localStorage
  };

  useEffect(() => {
    console.log('Cookies:', document.cookie);
  }, []);
  
  // Handle logout, clear state and localStorage
  const handleLogout = async () => {
    try {
      await fetch('http://localhost:5000/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      setIsAuthenticated(false);
      localStorage.removeItem('isAuthenticated'); // Remove authentication status from localStorage
    } catch (err) {
      console.error('Logout failed');
    }
  };

  return (
    <>
      <h1>Pare-Down App</h1>
      {
        isAuthenticated
        ?
        <>
          <DataForm />
          <button onClick={handleLogout}>Log Out</button>
        </>
        :
        <LoginForm onLoginSuccess={handleLoginSuccess} />
      }
    </>
  )
}

export default App;