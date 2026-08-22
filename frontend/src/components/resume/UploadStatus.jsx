/**
 * UploadStatus — shows upload success/error with resume details.
 */
import React from 'react';
import { getScoreColor } from '../../utils/helpers';

export default function UploadStatus({ result, error }) {
  if (error) {
    return (
      <div className="glass-card border-brand-rose/30 p-6 slide-up">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-full bg-brand-rose/10 flex items-center justify-center">
            <svg className="w-5 h-5 text-brand-rose" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          <div>
            <p className="text-text-primary font-medium">Upload Failed</p>
            <p className="text-brand-rose text-sm">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!result) return null;

  return (
    <div className="glass-card border-brand-emerald/30 p-6 slide-up">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-full bg-brand-emerald/10 flex items-center justify-center">
          <svg className="w-5 h-5 text-brand-emerald" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <p className="text-text-primary font-medium">Resume Uploaded Successfully</p>
          <p className="text-text-secondary text-sm">{result.filename}</p>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-4 text-center">
        <div className="p-3 rounded-lg bg-white/[0.02]">
          <p className={`text-2xl font-bold ${getScoreColor(result.ats_score)}`}>{result.ats_score}%</p>
          <p className="text-xs text-text-secondary mt-1">ATS Score</p>
        </div>
        <div className="p-3 rounded-lg bg-white/[0.02]">
          <p className="text-2xl font-bold text-brand-primary">{result.extracted_skills?.length || 0}</p>
          <p className="text-xs text-text-secondary mt-1">Skills Detected</p>
        </div>
      </div>
    </div>
  );
}
