import { create } from 'zustand';
import { notificationService } from '../services/notificationService';

export const useNotificationStore = create((set, get) => ({
  notifications: [],
  unreadCount: 0,
  isLoading: false,

  fetchNotifications: async (userId) => {
    if (!userId) return;
    
    set({ isLoading: true });
    try {
      const notifications = await notificationService.getNotifications(userId);
      const unreadCount = notifications.filter(n => !n.read).length;
      
      set({
        notifications,
        unreadCount,
        isLoading: false
      });
    } catch (error) {
      console.error('Failed to fetch notifications:', error);
      set({ isLoading: false });
    }
  },

  markAsRead: async (notificationId) => {
    try {
      await notificationService.markAsRead(notificationId);
      
      const notifications = get().notifications.map(n =>
        n.id === notificationId ? { ...n, read: true } : n
      );
      
      const unreadCount = notifications.filter(n => !n.read).length;
      
      set({ notifications, unreadCount });
    } catch (error) {
      console.error('Failed to mark notification as read:', error);
    }
  },

  markAllAsRead: async (userId) => {
    try {
      await notificationService.markAllAsRead(userId);
      
      const notifications = get().notifications.map(n => ({ ...n, read: true }));
      
      set({
        notifications,
        unreadCount: 0
      });
    } catch (error) {
      console.error('Failed to mark all notifications as read:', error);
    }
  },

  addNotification: (notification) => {
    const notifications = [notification, ...get().notifications];
    const unreadCount = notifications.filter(n => !n.read).length;
    
    set({
      notifications,
      unreadCount
    });
  }
}));