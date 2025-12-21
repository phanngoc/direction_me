/**
 * Utility functions for MyWay Career Assessment Frontend
 */

// API configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Local storage keys
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'myway_access_token',
  USER_DATA: 'myway_user_data',
  ASSESSMENT_PROGRESS: 'myway_assessment_progress',
  CURRENT_ASSESSMENT: 'myway_current_assessment'
} as const;

// Validation functions
export const validateEmail = (email: string): boolean => {
  const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return pattern.test(email);
};

export const validatePassword = (password: string): boolean => {
  // Password must be 8-50 characters
  if (password.length < 8 || password.length > 50) return false;
  
  const hasLetter = /[a-zA-Z]/.test(password);
  const hasNumber = /\d/.test(password);
  
  return hasLetter && hasNumber;
};

export const validateAge = (age: number): boolean => {
  return age >= 16 && age <= 25;
};

// Format functions
export const formatScore = (score: number, decimals: number = 2): string => {
  return score.toFixed(decimals);
};

export const formatPercentage = (value: number, total: number): string => {
  if (total === 0) return '0%';
  return `${((value / total) * 100).toFixed(1)}%`;
};

export const formatDate = (date: string | Date): string => {
  const d = new Date(date);
  return d.toLocaleDateString('vi-VN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

export const formatDateTime = (date: string | Date): string => {
  const d = new Date(date);
  return d.toLocaleString('vi-VN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// Local storage functions
export const getFromStorage = <T>(key: string): T | null => {
  if (typeof window === 'undefined') return null;
  
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : null;
  } catch {
    return null;
  }
};

export const setToStorage = <T>(key: string, value: T): void => {
  if (typeof window === 'undefined') return;
  
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    console.error('Error saving to localStorage:', error);
  }
};

export const removeFromStorage = (key: string): void => {
  if (typeof window === 'undefined') return;
  
  try {
    localStorage.removeItem(key);
  } catch (error) {
    console.error('Error removing from localStorage:', error);
  }
};

// API helper functions
export const getAuthHeaders = (): Record<string, string> => {
  const token = getFromStorage<string>(STORAGE_KEYS.ACCESS_TOKEN);
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const handleApiError = (error: any): string => {
  if (error.response?.data?.message) {
    return error.response.data.message;
  }
  if (error.message) {
    return error.message;
  }
  return 'Đã xảy ra lỗi không xác định';
};

// Assessment helper functions
export const getCategoryDisplayName = (category: string): string => {
  const names: Record<string, string> = {
    'IQ': 'Intelligence Quotient',
    'EQ': 'Emotional Quotient',
    'DQ': 'Digital Quotient',
    'AQ': 'Adversity Quotient'
  };
  return names[category] || category;
};

export const getFacetDisplayName = (facet: string): string => {
  const names: Record<string, string> = {
    'iq_lr': 'Logical Reasoning',
    'iq_nr': 'Numerical Reasoning',
    'iq_vr': 'Verbal Reasoning',
    'iq_sr': 'Spatial Reasoning',
    'eq_empathy': 'Empathy',
    'eq_social': 'Social Skills',
    'eq_self_awareness': 'Self-Awareness',
    'eq_self_regulation': 'Self-Regulation',
    'dq_info_literacy': 'Information Literacy',
    'dq_creativity': 'Creativity',
    'dq_safety': 'Safety',
    'dq_collaboration': 'Collaboration',
    'aq_control': 'Control',
    'aq_ownership': 'Ownership',
    'aq_reach': 'Reach',
    'aq_endurance': 'Endurance'
  };
  return names[facet] || facet;
};

// Chart helper functions
export const generateRadarChartData = (scores: {
  iq_score: number;
  eq_score: number;
  dq_score: number;
  aq_score: number;
}) => {
  return {
    labels: ['IQ', 'EQ', 'DQ', 'AQ'],
    datasets: [{
      label: 'Scores',
      data: [scores.iq_score, scores.eq_score, scores.dq_score, scores.aq_score],
      backgroundColor: 'rgba(59, 130, 246, 0.2)',
      borderColor: 'rgba(59, 130, 246, 1)',
      borderWidth: 2
    }]
  };
};

export const generateIkigaiChartData = (ikigai: {
  ikigai_love: number;
  ikigai_good_at: number;
  ikigai_world_needs: number;
  ikigai_paid_for: number;
}) => {
  return {
    labels: ['Love', 'Good at', 'World needs', 'Paid for'],
    datasets: [{
      label: 'Ikigai Scores',
      data: [
        ikigai.ikigai_love,
        ikigai.ikigai_good_at,
        ikigai.ikigai_world_needs,
        ikigai.ikigai_paid_for
      ],
      backgroundColor: 'rgba(16, 185, 129, 0.2)',
      borderColor: 'rgba(16, 185, 129, 1)',
      borderWidth: 2
    }]
  };
};

// Progress helper functions
export const calculateProgress = (current: number, total: number): number => {
  if (total === 0) return 0;
  return Math.round((current / total) * 100);
};

export const getProgressColor = (progress: number): string => {
  if (progress < 30) return 'text-red-600';
  if (progress < 70) return 'text-yellow-600';
  return 'text-green-600';
};

// Time helper functions
export const formatDuration = (minutes: number): string => {
  if (minutes < 60) {
    return `${minutes} phút`;
  }
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  return `${hours} giờ ${remainingMinutes} phút`;
};

export const getTimeRemaining = (startTime: Date, totalMinutes: number): number => {
  const elapsed = (Date.now() - startTime.getTime()) / (1000 * 60);
  return Math.max(0, totalMinutes - elapsed);
};

// String helper functions
export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength - 3) + '...';
};

export const capitalizeFirst = (text: string): string => {
  return text.charAt(0).toUpperCase() + text.slice(1);
};

export const slugify = (text: string): string => {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9 -]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .trim('-');
};

// Array helper functions
export const shuffleArray = <T>(array: T[]): T[] => {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
};

export const chunkArray = <T>(array: T[], size: number): T[][] => {
  const chunks: T[][] = [];
  for (let i = 0; i < array.length; i += size) {
    chunks.push(array.slice(i, i + size));
  }
  return chunks;
};

// Debounce function
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
};