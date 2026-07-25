import React from 'react';
import { useNavigate } from 'react-router-dom';
import Input from '../Forms/Input';
import Button from '../Forms/Button';
import Alert from '../Common/Alert';
import { authService } from '../../services';
import useStore from '../../store/useStore';

const LoginPage = () => {
  const navigate = useNavigate();
  const { login } = useStore();
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [error, setError] = React.useState('');
  const [loading, setLoading] = React.useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authService.login(email, password);
      const { access_token, user: userData } = response.data.data;

      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(userData));

      login(userData, access_token);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary via-secondary to-primary flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-secondary/40 backdrop-blur-xl border border-cyan-500/20 rounded-lg p-8">
          <h1 className="text-3xl font-bold text-cyan-400 mb-2">VehicleGate</h1>
          <p className="text-gray-400 mb-8">AI Smart Access System</p>

          {error && <Alert type="error" message={error} onClose={() => setError('')} />}

          <form onSubmit={handleLogin} className="space-y-4">
            <Input
              label="Email"
              type="email"
              placeholder="admin@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <Input
              label="Password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <Button
              type="submit"
              disabled={loading}
              size="lg"
              className="w-full"
            >
              {loading ? 'Logging in...' : 'Login'}
            </Button>
          </form>

          <p className="text-gray-400 text-sm mt-4 text-center">
            Demo Credentials:<br />
            admin@example.com / admin123
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
