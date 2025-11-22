import api from './api';

export const authService = {
  async login(email, password) {
    const res = await api.post('/auth/login', { email, password });
    return res.data.data;
  },

  async register(userData) {
    const res = await api.post('/auth/register', userData);
    return res.data.data;
  },

  async getCurrentUser() {
    const res = await api.get('/auth/profile');
    return res.data.data.user;
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
};