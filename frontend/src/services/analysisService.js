/**
 * Analysis API service — handles analysis runs, history, and details.
 */
import api from './api';

const analysisService = {
  async runAnalysis(resumeId, selectedRoles) {
    return api.post('/analysis/run', {
      resume_id: resumeId,
      selected_roles: selectedRoles,
    });
  },

  async getHistory(limit = 10, offset = 0) {
    return api.get(`/analysis/history?limit=${limit}&offset=${offset}`);
  },

  async getById(analysisId) {
    return api.get(`/analysis/${analysisId}`);
  },
};

export default analysisService;
