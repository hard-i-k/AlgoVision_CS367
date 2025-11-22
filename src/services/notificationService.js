import api from './api';

// Mock data for development
let MOCK_NOTIFICATIONS = [
  {
    id: 1,
    userId: 1,
    type: 'answer',
    title: 'New answer on your question',
    message: 'admin answered your question "How to center a div in CSS?"',
    read: false,
    createdAt: '2024-01-15T11:00:00Z',
    relatedId: 1
  },
  {
    id: 2,
    userId: 1,
    type: 'mention',
    title: 'You were mentioned',
    message: 'admin mentioned you in a comment',
    read: false,
    createdAt: '2024-01-15T10:45:00Z',
    relatedId: 2
  }
];

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export const notificationService = {
  async getNotifications(userId) {
    await delay(200);
    return MOCK_NOTIFICATIONS
      .filter(n => n.userId === parseInt(userId))
      .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  },

  async markAsRead(notificationId) {
    await delay(100);
    const notification = MOCK_NOTIFICATIONS.find(n => n.id === parseInt(notificationId));
    if (notification) {
      notification.read = true;
    }
    return notification;
  },

  async markAllAsRead(userId) {
    await delay(200);
    MOCK_NOTIFICATIONS.forEach(n => {
      if (n.userId === parseInt(userId)) {
        n.read = true;
      }
    });
    return true;
  },

  async getUnreadCount(userId) {
    await delay(100);
    return MOCK_NOTIFICATIONS.filter(n => n.userId === parseInt(userId) && !n.read).length;
  }
};