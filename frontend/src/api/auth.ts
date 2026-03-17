const API_BASE = '/api';

interface AuthResponse {
  token: string;
  user: { id: number; username: string; email: string };
}

interface PasswordResetRequest {
  email: string;
}

export const authApi = {
  register: async (username: string, email: string, password: string): Promise<AuthResponse> => {
    const res = await fetch(`${API_BASE}/auth/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password }),
    });
    if (!res.ok) throw new Error('Registration failed');
    return res.json();
  },

  login: async (username: string, password: string): Promise<AuthResponse> => {
    const res = await fetch(`${API_BASE}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) throw new Error('Login failed');
    return res.json();
  },

  requestPasswordReset: async (email: string): Promise<{ message: string }> => {
    const res = await fetch(`${API_BASE}/auth/password-reset/request/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    if (!res.ok) throw new Error('Password reset request failed');
    return res.json();
  },

  confirmPasswordReset: async (token: string, new_password: string): Promise<{ message: string }> => {
    const res = await fetch(`${API_BASE}/auth/password-reset/confirm/${token}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ new_password }),
    });
    if (!res.ok) throw new Error('Password reset confirmation failed');
    return res.json();
  },
};
