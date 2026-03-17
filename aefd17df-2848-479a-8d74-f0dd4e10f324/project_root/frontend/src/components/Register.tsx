import React, { useState } from 'react'

interface RegisterFormData {
  username: string
  email: string
  password: string
}

interface RegisterProps {
  onSuccess?: () => void
}

const Register: React.FC<RegisterProps> = ({ onSuccess }) => {
  const [formData, setFormData] = useState<RegisterFormData>({
    username: '',
    email: '',
    password: ''
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [success, setSuccess] = useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })
      
      const data = await response.json()
      
      if (response.ok) {
        setSuccess('Registration successful')
        localStorage.setItem('token', data.token)
        if (onSuccess) onSuccess()
      } else {
        setErrors(data)
      }
    } catch (error) {
      setErrors({ general: 'Something went wrong' })
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Register</h2>
      
      {success && <div data-cy="success-message" className="success">{success}</div>}
      {errors.general && <div data-cy="error-message" className="error">{errors.general}</div>}
      
      <div>
        <label>Username:</label>
        <input 
          data-cy="username-input"
          type="text" 
          name="username" 
          value={formData.username} 
          onChange={handleChange}
        />
        {errors.username && <div data-cy="username-error" className="error">{errors.username}</div>}
      </div>

      <div>
        <label>Email:</label>
        <input 
          data-cy="email-input"
          type="email" 
          name="email" 
          value={formData.email} 
          onChange={handleChange}
        />
        {errors.email && <div data-cy="email-error" className="error">{errors.email}</div>}
      </div>

      <div>
        <label>Password:</label>
        <input 
          data-cy="password-input"
          type="password" 
          name="password" 
          value={formData.password} 
          onChange={handleChange}
        />
        {errors.password && <div data-cy="password-error" className="error">{errors.password}</div>}
      </div>

      <button data-cy="register-button" type="submit">Register</button>
    </form>
  )
}

export default Register
