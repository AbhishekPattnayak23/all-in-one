import { useEffect, useState } from 'react';
import axios from 'axios';

interface User {
  id: string;
  username: string;
  email: string;
  created_at: string;
}

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('jwt');
    const base = import.meta.env.VITE_API_BASE_URL || '';
    axios.get(`${base}/api/user/me/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(res => {
        setUser(res.data);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div id="dashboard">Loading...</div>;
  if (!user) return <div id="dashboard"><p>Error loading user data</p></div>;

  return (
    <div id="dashboard">
      <h1>Welcome, {user.username}</h1>
      <p>Email: {user.email}</p>
    </div>
  );
}
