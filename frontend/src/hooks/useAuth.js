import { useEffect, useState } from 'react';
import useStore from '../store/useStore';
import { authService } from '../services';

export const useAuth = () => {
  const [loading, setLoading] = useState(true);
  const { user, token, isAuthenticated, setUser, setToken, login, logout } = useStore();

  useEffect(() => {
    useStore.getState().loadFromStorage();
    setLoading(false);
  }, []);

  const handleLogin = async (email, password) => {
    try {
      const response = await authService.login(email, password);
      const { access_token, user: userData } = response.data.data;
      
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(userData));
      
      login(userData, access_token);
      return userData;
    } catch (error) {
      throw error;
    }
  };

  const handleLogout = () => {
    authService.logout();
    logout();
  };

  return {
    user,
    token,
    isAuthenticated,
    loading,
    login: handleLogin,
    logout: handleLogout,
  };
};

export const useFetch = (fetchFn, dependencies = []) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetchFn();
        setData(response.data.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, dependencies);

  return { data, loading, error };
};
