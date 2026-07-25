import React from 'react';
import { Moon, Sun } from 'lucide-react';
import useStore from '../../store/useStore';

const ThemeToggle = () => {
  const { darkMode, setDarkMode } = useStore();

  return (
    <button
      onClick={() => setDarkMode(!darkMode)}
      className="p-2 rounded-lg bg-secondary hover:bg-opacity-80 transition"
      title="Toggle dark mode"
    >
      {darkMode ? <Sun size={20} /> : <Moon size={20} />}
    </button>
  );
};

export default ThemeToggle;
