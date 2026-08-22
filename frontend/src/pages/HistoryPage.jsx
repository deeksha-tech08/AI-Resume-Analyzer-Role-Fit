/**
 * HistoryPage — paginated analysis history table.
 */
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/common/Button';
import Loading from '../components/common/Loading';
import ErrorMessage from '../components/common/ErrorMessage';
import useAnalysis from '../hooks/useAnalysis';
import { formatDate, getScoreColor } from '../utils/helpers';

export default function HistoryPage() {
  const navigate = useNavigate();
  const { history, pagination, loading, error, fetchHistory } = useAnalysis();
  const [currentPage, setCurrentPage] = useState(0);
  const limit = 10;

  useEffect(() => {
    fetchHistory(limit, currentPage * limit);
  }, [currentPage, fetchHistory]);

  const totalPages = Math.ceil((pagination.total || 0) / limit);

  if (loading && history.length === 0) return <Loading message="Loading history..." />;

  return (
    <div className="flex-1 py-8 px-4 max-w-5xl mx-auto w-full">
      <div className="text-center mb-8 slide-up">
        <h1 className="text-3xl font-bold gradient-text mb-2">Analysis History</h1>
        <p className="text-text-secondary">Review your past resume analyses</p>
      </div>

      {error && <ErrorMessage message={error} onRetry={() => fetchHistory(limit, currentPage * limit)} />}

      {history.length === 0 && !loading ? (
        <div className="glass-card p-8 text-center slide-up">
          <p className="text-text-secondary mb-4">No analyses yet. Upload a resume to get started.</p>
          <Button onClick={() => navigate('/upload')}>Upload Resume</Button>
        </div>
      ) : (
        <>
          {/* Desktop Table */}
          <div className="hidden md:block glass-card overflow-hidden slide-up">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border-subtle">
                  <th className="text-left px-6 py-4 text-xs font-semibold text-text-secondary uppercase tracking-wider">Resume</th>
                  <th className="text-center px-4 py-4 text-xs font-semibold text-text-secondary uppercase tracking-wider">ATS</th>
                  <th className="text-left px-4 py-4 text-xs font-semibold text-text-secondary uppercase tracking-wider">Best Role</th>
                  <th className="text-center px-4 py-4 text-xs font-semibold text-text-secondary uppercase tracking-wider">Fit %</th>
                  <th className="text-center px-4 py-4 text-xs font-semibold text-text-secondary uppercase tracking-wider">Date</th>
                  <th className="text-center px-4 py-4 text-xs font-semibold text-text-secondary uppercase tracking-wider">Action</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item) => (
                  <tr key={item.id} className="border-b border-border-subtle/50 hover:bg-white/[0.02] transition-colors">
                    <td className="px-6 py-4 text-sm text-text-primary font-medium truncate max-w-[200px]">{item.resume_filename}</td>
                    <td className={`px-4 py-4 text-sm text-center font-bold ${getScoreColor(item.ats_score)}`}>{item.ats_score}%</td>
                    <td className="px-4 py-4 text-sm text-text-primary">{item.best_fit_role}</td>
                    <td className={`px-4 py-4 text-sm text-center font-bold ${getScoreColor(item.best_fit_score)}`}>{item.best_fit_score}%</td>
                    <td className="px-4 py-4 text-sm text-text-secondary text-center">{formatDate(item.created_at)}</td>
                    <td className="px-4 py-4 text-center">
                      <button
                        onClick={() => navigate(`/results/${item.id}`)}
                        className="text-brand-primary hover:text-brand-secondary text-sm font-medium transition-colors"
                      >
                        View →
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Mobile Cards */}
          <div className="md:hidden space-y-3">
            {history.map((item) => (
              <div key={item.id} className="glass-card p-4 slide-up" onClick={() => navigate(`/results/${item.id}`)}>
                <div className="flex justify-between items-start mb-2">
                  <p className="text-text-primary font-medium text-sm truncate max-w-[60%]">{item.resume_filename}</p>
                  <span className="text-text-secondary text-xs">{formatDate(item.created_at)}</span>
                </div>
                <div className="flex items-center gap-4 text-sm">
                  <span className={`font-bold ${getScoreColor(item.ats_score)}`}>ATS: {item.ats_score}%</span>
                  <span className="text-text-secondary">|</span>
                  <span className="text-text-primary">{item.best_fit_role}</span>
                  <span className={`font-bold ${getScoreColor(item.best_fit_score)}`}>{item.best_fit_score}%</span>
                </div>
              </div>
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-3 mt-6">
              <Button
                variant="ghost"
                size="sm"
                disabled={currentPage === 0}
                onClick={() => setCurrentPage(p => p - 1)}
              >
                ← Previous
              </Button>
              <span className="text-text-secondary text-sm">
                Page {currentPage + 1} of {totalPages}
              </span>
              <Button
                variant="ghost"
                size="sm"
                disabled={currentPage >= totalPages - 1}
                onClick={() => setCurrentPage(p => p + 1)}
              >
                Next →
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
