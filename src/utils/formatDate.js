import { format, formatDistanceToNow, isToday, isYesterday } from 'date-fns';

export const formatDate = (date) => {
  const dateObj = new Date(date);
  
  if (isToday(dateObj)) {
    return `Today at ${format(dateObj, 'HH:mm')}`;
  }
  
  if (isYesterday(dateObj)) {
    return `Yesterday at ${format(dateObj, 'HH:mm')}`;
  }
  
  const daysAgo = formatDistanceToNow(dateObj, { addSuffix: true });
  
  if (daysAgo.includes('day')) {
    return format(dateObj, 'MMM d, yyyy');
  }
  
  return daysAgo;
};

export const formatDateLong = (date) => {
  return format(new Date(date), 'MMMM d, yyyy \'at\' HH:mm');
};