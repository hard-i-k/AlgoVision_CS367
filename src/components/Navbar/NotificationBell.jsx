import React, { useState, useEffect } from 'react';
import { BellIcon } from '@heroicons/react/24/outline';
import { useNotificationStore } from '../../context/notificationStore';
import { useAuthStore } from '../../context/authStore';
import NotificationDropdown from './NotificationDropdown';

const NotificationBell = () => {
  const [showDropdown, setShowDropdown] = useState(false);
  const { unreadCount = 0, fetchNotifications } = useNotificationStore();
  const { user = null } = useAuthStore();

  useEffect(() => {
    if (user) {
      fetchNotifications(user.id);
    }
  }, [user]);

  return (
    <div className="relative">
      <button
        onClick={() => setShowDropdown(!showDropdown)}
        className="relative p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <BellIcon className="h-6 w-6" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {showDropdown && (
        <NotificationDropdown onClose={() => setShowDropdown(false)} />
      )}
    </div>
  );
};

export default NotificationBell;