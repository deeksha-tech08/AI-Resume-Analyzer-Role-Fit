/**
 * UploadProgress — shows upload and processing progress.
 */
import React from 'react';

export default function UploadProgress({ stage = 'uploading' }) {
  const stages = [
    { key: 'uploading', label: 'Uploading PDF...' },
    { key: 'extracting', label: 'Extracting text...' },
    { key: 'analyzing', label: 'Analyzing skills & ATS...' },
    { key: 'done', label: 'Complete!' },
  ];

  const currentIdx = stages.findIndex(s => s.key === stage);

  return (
    <div className="glass-card p-6 slide-up">
      <div className="space-y-3">
        {stages.map((s, idx) => (
          <div key={s.key} className="flex items-center gap-3">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 ${
              idx < currentIdx ? 'bg-brand-emerald/20 text-brand-emerald' :
              idx === currentIdx ? 'bg-brand-primary/20 text-brand-primary animate-pulse' :
              'bg-white/5 text-text-secondary'
            }`}>
              {idx < currentIdx ? '✓' : idx + 1}
            </div>
            <span className={`text-sm ${idx <= currentIdx ? 'text-text-primary' : 'text-text-secondary'}`}>
              {s.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
