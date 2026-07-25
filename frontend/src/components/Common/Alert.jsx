import React from 'react';
import { AlertCircle, CheckCircle, InfoIcon, AlertTriangle } from 'lucide-react';

const Alert = ({ type = 'info', title, message, onClose }) => {
  const styles = {
    success: 'bg-green-500/20 border-green-500 text-green-200',
    error: 'bg-red-500/20 border-red-500 text-red-200',
    warning: 'bg-yellow-500/20 border-yellow-500 text-yellow-200',
    info: 'bg-blue-500/20 border-blue-500 text-blue-200',
  };

  const icons = {
    success: <CheckCircle size={20} />,
    error: <AlertCircle size={20} />,
    warning: <AlertTriangle size={20} />,
    info: <InfoIcon size={20} />,
  };

  React.useEffect(() => {
    if (onClose) {
      const timer = setTimeout(onClose, 5000);
      return () => clearTimeout(timer);
    }
  }, [onClose]);

  return (
    <div className={`border rounded-lg p-4 ${styles[type]} backdrop-blur-xl flex gap-3`}>
      <div className="flex-shrink-0">{icons[type]}</div>
      <div className="flex-1">
        {title && <div className="font-semibold">{title}</div>}
        {message && <div className="text-sm opacity-90">{message}</div>}
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="flex-shrink-0 opacity-70 hover:opacity-100 transition"
        >
          ✕
        </button>
      )}
    </div>
  );
};

export default Alert;
