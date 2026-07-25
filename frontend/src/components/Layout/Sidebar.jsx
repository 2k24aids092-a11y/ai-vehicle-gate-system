import React from 'react';
import { LayoutDashboard, Video, Car, Users, ParkingCircle, FileText, Bell, Settings, LogOut, Menu, X } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

const Sidebar = ({ open, setOpen }) => {
  const navigate = useNavigate();
  const { logout, user } = useAuth();

  const menuItems = [
    { icon: LayoutDashboard, label: 'Dashboard', path: '/dashboard' },
    { icon: Video, label: 'Live Camera', path: '/camera' },
    { icon: Car, label: 'Vehicles', path: '/vehicles' },
    { icon: Users, label: 'Visitors', path: '/visitors' },
    { icon: ParkingCircle, label: 'Parking', path: '/parking' },
    { icon: FileText, label: 'Reports', path: '/reports' },
    { icon: Bell, label: 'Alerts', path: '/alerts' },
    { icon: Settings, label: 'Settings', path: '/settings' },
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={() => setOpen(!open)}
        className="fixed top-4 left-4 z-50 md:hidden p-2 bg-secondary rounded-lg"
      >
        {open ? <X /> : <Menu />}
      </button>

      {/* Sidebar */}
      <div
        className={`fixed left-0 top-0 h-full w-64 bg-primary/95 backdrop-blur border-r border-cyan-500/20 transform transition-transform duration-300 z-40 ${
          open ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        }`}
      >
        <div className="p-6 border-b border-cyan-500/20">
          <h1 className="text-2xl font-bold text-cyan-400">VehicleGate</h1>
          <p className="text-gray-400 text-sm">Access System</p>
        </div>

        {/* User info */}
        <div className="p-4 border-b border-cyan-500/20">
          <p className="text-gray-400 text-xs uppercase">Logged in as</p>
          <p className="text-white font-semibold">{user?.name}</p>
          <p className="text-cyan-400 text-xs mt-1">{user?.role}</p>
        </div>

        {/* Navigation */}
        <nav className="p-4 space-y-2 flex-1">
          {menuItems.map((item) => (
            <button
              key={item.path}
              onClick={() => {
                navigate(item.path);
                setOpen(false);
              }}
              className="w-full flex items-center gap-3 px-4 py-2 rounded-lg text-gray-300 hover:bg-cyan-500/20 hover:text-cyan-400 transition"
            >
              <item.icon size={20} />
              <span>{item.label}</span>
            </button>
          ))}
        </nav>

        {/* Logout */}
        <div className="p-4 border-t border-cyan-500/20">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-2 rounded-lg text-red-400 hover:bg-red-500/20 transition"
          >
            <LogOut size={20} />
            <span>Logout</span>
          </button>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
