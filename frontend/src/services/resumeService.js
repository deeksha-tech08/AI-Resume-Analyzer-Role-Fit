/**
 * Resume API service — handles resume upload and retrieval.
 */
import api from './api';

const resumeService = {
  async upload(file) {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/resume/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  async getLatest() {
    return api.get('/resume/latest');
  },

  async getById(resumeId) {
    return api.get(`/resume/${resumeId}`);
  },
};

export default resumeService;
