/**
 * ResultsPage — displays full analysis results, loads by ID.
 */
import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ResultsDashboard from '../components/results/ResultsDashboard';
import Loading from '../components/common/Loading';
import ErrorMessage from '../components/common/ErrorMessage';
import Button from '../components/common/Button';
import useAnalysis from '../hooks/useAnalysis';

export default function ResultsPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { analysis, loading, error, fetchAnalysis } = useAnalysis();

  useEffect(() => {
    if (id) {
      fetchAnalysis(id);
    }
  }, [id, fetchAnalysis]);

  if (loading) return <Loading message="Loading analysis results..." />;

  if (error) {
    return (
      <div className="flex-1 flex items-center justify-center py-12">
        <ErrorMessage message={error} onRetry={() => id && fetchAnalysis(id)} />
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="flex-1 flex items-center justify-center py-12">
        <div className="glass-card p-8 text-center max-w-md">
          <p className="text-text-secondary mb-4">No analysis data found.</p>
          <Button onClick={() => navigate('/upload')}>Upload a Resume</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 py-8 px-4">
      <div className="text-center mb-8 slide-up">
        <h1 className="text-3xl font-bold gradient-text mb-2">Analysis Results</h1>
        <p className="text-text-secondary">Your resume analysis is ready</p>
      </div>
      <ResultsDashboard analysis={analysis} />
      <div className="text-center mt-8 flex flex-wrap justify-center gap-4">
        <Button variant="secondary" onClick={() => navigate('/upload')}>
          Upload New Resume
        </Button>
        <Button variant="secondary" onClick={() => navigate('/history')}>
          View History
        </Button>
      </div>
    </div>
  );
}
