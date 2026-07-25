import React from 'react';
import { BarChart3, Users, Car, ParkingCircle, AlertCircle } from 'lucide-react';

const StatsCard = ({ title, value, icon: Icon, trend, color = 'accent' }) => {
  return (
    <div className="bg-secondary/40 backdrop-blur-xl border border-cyan-500/20 rounded-lg p-6 hover:border-cyan-500/50 transition">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-gray-400 text-sm">{title}</p>
          <h3 className="text-3xl font-bold text-white mt-2">{value}</h3>
          {trend && (
            <p className="text-green-400 text-sm mt-2">{trend}% ↑</p>
          )}
        </div>
        {Icon && (
          <div className={`p-3 rounded-lg bg-${color}-500/20`}>
            <Icon size={24} className={`text-${color}-400`} />
          </div>
        )}
      </div>
    </div>
  );
};

export default StatsCard;
