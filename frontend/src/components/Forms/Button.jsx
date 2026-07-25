import React from 'react';

const Button = ({ children, variant = 'primary', size = 'md', disabled, ...props }) => {
  const baseStyles = 'font-semibold rounded-lg transition duration-200 flex items-center justify-center gap-2';
  
  const variants = {
    primary: 'bg-cyan-500 hover:bg-cyan-600 text-white disabled:opacity-50',
    secondary: 'bg-secondary border border-cyan-500/50 hover:border-cyan-500 text-cyan-400 disabled:opacity-50',
    danger: 'bg-red-500 hover:bg-red-600 text-white disabled:opacity-50',
    ghost: 'hover:bg-secondary/50 text-gray-300 disabled:opacity-50',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]}`}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
