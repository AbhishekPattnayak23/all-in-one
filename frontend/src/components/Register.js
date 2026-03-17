import React, { useState } from 'react';
import axios from 'axios';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setSuccessMessage('');

    try {
      const response = await axios.post('/api/auth/register', {
        username: formData.username,
        email: formData.email,
        password: formData.password
      });
      
      setSuccessMessage('Registration successful! You can now log in.');
      setFormData({ username: '', email: '', password: '' });
    } catch (err) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Registration failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px' }}>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="username">Username:</label>
          <input 
            type="text" 
            id="username"
            name="username" 
            value={formData.username} 
            onChange={handleChange} 
            maxLength="32" 
            required 
            style={{ width: '100%', padding: '8px', marginTop: '5px', boxSizing: 'border-box' }} 
          />
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="email">Email:</label>
          <input 
            type="email" 
            id="email"
            name="email" 
            value={formData.email} 
            onChange={handleChange} 
            required 
            style={{ width: '100%', padding: '8px', marginTop: '5px', boxSizing: 'border-box' }} 
          />
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="password">Password:</label>
          <input 
            type="password" 
            id="password"
            name="password" 
            value={formData.password} 
            onChange={handleChange} 
            required 
            style={{ width: '100%', padding: '8px', marginTop: '5px', boxSizing: 'border-box' }} 
          />
        </div>
        
        <button 
          type="submit" 
          disabled={isLoading} 
          style={{ 
            width: '100%', 
            padding: '10px', 
            backgroundColor: '#007bff', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px', 
            cursor: 'pointer',
            boxSizing: 'border-box'
          }}
        >
          {isLoading ? 'Registering...' : 'Register'}
        </button>
      </form>
      
      {error && (
        <div style={{ color: 'red', marginTop: '10px', padding: '10px', border: '1px solid red', borderRadius: '4px' }}>
          Error: {error}
        </div>
      )}
      
      {successMessage && (
        <div style={{ color: 'green', marginTop: '10px', padding: '10px', border: '1px solid green', borderRadius: '4px' }}>
          {successMessage}
        </div>
      )}
    </div>
  );
};

export default Register;
