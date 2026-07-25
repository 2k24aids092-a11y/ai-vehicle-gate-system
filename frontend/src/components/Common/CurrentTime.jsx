import React from 'react';
import { Clock } from 'lucide-react';

const CurrentTime = () => {
  const [time, setTime] = React.useState(new Date());

  React.useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="flex items-center gap-2 text-cyan-400">
      <Clock size={16} />
      <span className="font-mono">{time.toLocaleTimeString()}</span>
    </div>
  );
};

export default CurrentTime;
