/**
 * useAnalysis hook — manages analysis state and API calls.
 */
import { useState, useCallback } from 'react';
import analysisService from '../services/analysisService';

export default function useAnalysis() {
  const [analysis, setAnalysis] = useState(null);
  const [history, setHistory] = useState([]);
  const [pagination, setPagination] = useState({ total: 0, limit: 10, offset: 0 });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const runAnalysis = useCallback(async (resumeId, selectedRoles) => {
    setLoading(true);
    setError('');
    try {
      const response = await analysisService.runAnalysis(resumeId, selectedRoles);
      if (response?.success) {
        setAnalysis(response.data);
        return response.data;
      }
      throw new Error(response?.error || 'Analysis failed');
    } catch (err) {
      setError(err.message || 'Failed to run analysis');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchHistory = useCallback(async (limit = 10, offset = 0) => {
    setLoading(true);
    setError('');
    try {
      const response = await analysisService.getHistory(limit, offset);
      if (response?.success) {
        setHistory(response.data || []);
        setPagination(response.pagination || { total: 0, limit, offset });
        return response.data;
      }
    } catch (err) {
      setError(err.message || 'Failed to load history');
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchAnalysis = useCallback(async (analysisId) => {
    setLoading(true);
    setError('');
    try {
      const response = await analysisService.getById(analysisId);
      if (response?.success) {
        setAnalysis(response.data);
        return response.data;
      }
    } catch (err) {
      setError(err.message || 'Failed to load analysis');
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    analysis, history, pagination, loading, error,
    runAnalysis, fetchHistory, fetchAnalysis,
    setAnalysis, setError,
  };
}
