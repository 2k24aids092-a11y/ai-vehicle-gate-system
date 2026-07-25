import React from 'react';
import Sidebar from './Sidebar';
import CurrentTime from '../Common/CurrentTime';
import ThemeToggle from '../Common/ThemeToggle';

const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = React.useState(false);

  return (
    <div className="flex bg-primary text-white min-h-screen">
      <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />

      <div className="flex-1 md:ml-64">
        {/* Top bar */}
        <div className="bg-secondary/40 backdrop-blur border-b border-cyan-500/20 p-4 flex justify-between items-center sticky top-0 z-30">
          <div className="flex-1" />
          <div className="flex items-center gap-4">
            <CurrentTime />
            <ThemeToggle />
          </div>
        </div>

        {/* Main content */}
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
