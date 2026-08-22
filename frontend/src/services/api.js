/**
 * Axios instance configured with base URL and HTTP-only cookie support.
 * Response interceptor handles 401 redirects and unwraps response data.
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor: unwrap data or handle errors
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    if (error.response) {
      // Server responded with error status
      if (error.response.status === 401) {
        // Only redirect if not already on auth pages
        const currentPath = window.location.pathname;
        if (currentPath !== '/login' && currentPath !== '/register' && currentPath !== '/') {
          window.location.href = '/login';
        }
      }
      // Return the error data from the server for display
      const serverError = error.response.data;
      return Promise.reject({
        message: serverError?.error || serverError?.detail || 'An error occurred',
        status: error.response.status,
        data: serverError,
      });
    }
    // Network error or timeout
    return Promise.reject({
      message: 'Network error. Please check your connection.',
      status: 0,
      data: null,
    });
  }
);

export default api;
