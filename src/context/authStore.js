import { create } from 'zustand';
import { authService } from '../services/authService';

export const useAuthStore = create((set, get) => ({
  user: null,
  token: null,
  isLoading: false,
  isAuthenticated: false,

  // Initialize auth state from localStorage
  initialize: () => {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
      set({
        token,
        user: JSON.parse(user),
        isAuthenticated: true
      });
    }
  },

  login: async (email, password) => {
    set({ isLoading: true });
    try {
      const { user, token } = await authService.login(email, password);
      
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(user));
      
      set({
        user,
        token,
        isAuthenticated: true,
        isLoading: false
      });
      
      return { success: true };
    } catch (error) {
      set({ isLoading: false });
      return { success: false, error: error.message };
    }
  },

  register: async (userData) => {
    set({ isLoading: true });
    try {
      const { user, token } = await authService.register(userData);
      
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(user));
      
      set({
        user,
        token,
        isAuthenticated: true,
        isLoading: false
      });
      
      return { success: true };
    } catch (error) {
      set({ isLoading: false });
      return { success: false, error: error.message };
    }
  },

  logout: () => {
    authService.logout();
    set({
      user: null,
      token: null,
      isAuthenticated: false
    });
  },

  updateUser: (userData) => {
    const updatedUser = { ...get().user, ...userData };
    localStorage.setItem('user', JSON.stringify(updatedUser));
    set({ user: updatedUser });
  }
}));