import React from 'react';
import Layout from '../components/Layout/Layout';
import StatsCard from '../components/Cards/StatsCard';
import { BarChart3, Users, Car, ParkingCircle, AlertCircle, TrendingUp } from 'lucide-react';
import { dashboardService, logService, parkingService } from '../services';

const Dashboard = () => {
  const [stats, setStats] = React.useState(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const [dashboardData, parkingData] = await Promise.all([
          dashboardService.getOverview(),
          parkingService.getParkingStatus(),
        ]);
        setStats({
          ...dashboardData.data.data,
          ...parkingData.data.data,
        });
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-400 mx-auto mb-4"></div>
            <p className="text-gray-400">Loading dashboard...</p>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">Dashboard</h1>
          <p className="text-gray-400">Welcome back! Here's your system overview.</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatsCard
            title="Today's Entries"
            value={stats?.today_entries || 0}
            icon={Car}
            trend={12}
          />
          <StatsCard
            title="Today's Exits"
            value={stats?.today_exits || 0}
            icon={TrendingUp}
          />
          <StatsCard
            title="Vehicles Inside"
            value={stats?.vehicles_inside || 0}
            icon={Car}
          />
          <StatsCard
            title="Parking Occupancy"
            value={`${stats?.parking_occupancy_percentage || 0}%`}
            icon={ParkingCircle}
          />
        </div>

        {/* Secondary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <StatsCard
            title="Parking Available"
            value={stats?.parking_available || 0}
            icon={ParkingCircle}
            color="green"
          />
          <StatsCard
            title="Total Parking"
            value={stats?.parking_total || 0}
            icon={ParkingCircle}
          />
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;
