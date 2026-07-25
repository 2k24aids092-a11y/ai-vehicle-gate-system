import api from './api';

export const authService = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (email, password, name, role) => 
    api.post('/auth/register', { email, password, name, role }),
  getCurrentUser: () => api.get('/auth/me'),
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
};

export const vehicleService = {
  getVehicles: (skip = 0, limit = 10, search = '') => 
    api.get('/vehicles', { params: { skip, limit, search } }),
  getVehicleById: (id) => api.get(`/vehicles/${id}`),
  createVehicle: (data) => api.post('/vehicles', data),
  updateVehicle: (id, data) => api.put(`/vehicles/${id}`, data),
  deleteVehicle: (id) => api.delete(`/vehicles/${id}`),
};

export const parkingService = {
  getParkingStatus: () => api.get('/parking/status'),
  getParkingSlots: () => api.get('/parking/slots'),
  assignParking: (vehicleId, slotNumber) => 
    api.post('/parking/assign', { vehicle_id: vehicleId, slot_number: slotNumber }),
  releaseParking: (slotId) => api.post(`/parking/release/${slotId}`),
};

export const logService = {
  getLogs: (skip = 0, limit = 10, days = 7) => 
    api.get('/logs', { params: { skip, limit, days } }),
  createLog: (data) => api.post('/logs', data),
  markExit: (logId) => api.post(`/logs/${logId}/exit`),
  getTodayStats: () => api.get('/logs/stats/today'),
};

export const dashboardService = {
  getOverview: () => api.get('/dashboard/overview'),
};
