/**
 * Auth API service — handles register, login, logout, and profile requests.
 */
import api from './api';

const authService = {
  async register(fullName, email, password) {
    return api.post('/auth/register', {
      full_name: fullName,
      email,
      password,
    });
  },

  async login(email, password) {
    return api.post('/auth/login', { email, password });
  },

  async getMe() {
    return api.get('/auth/me');
  },

  async logout() {
    return api.post('/auth/logout');
  },
};

export default authService;
