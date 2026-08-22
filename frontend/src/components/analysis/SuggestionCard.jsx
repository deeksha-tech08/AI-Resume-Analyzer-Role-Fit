/**
 * SuggestionCard — displays AI-generated improvement suggestions.
 */
import React from 'react';

export default function SuggestionCard({ suggestions = [] }) {
  if (!suggestions.length) return null;

  return (
    <div className="glass-card p-6 slide-up">
      <h3 className="text-lg font-semibold text-text-primary mb-4 flex items-center gap-2">
        <svg className="w-5 h-5 text-brand-amber" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 001.5-.189m-1.5.189a6.01 6.01 0 01-1.5-.189m3.75 7.478a12.06 12.06 0 01-4.5 0m3.75 2.383a14.406 14.406 0 01-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 10-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
        </svg>
        Improvement Suggestions
      </h3>
      <div className="space-y-3">
        {suggestions.map((suggestion, idx) => (
          <div key={idx} className="flex items-start gap-3 p-3 rounded-lg bg-white/[0.02] border border-border-subtle">
            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-brand-amber/10 text-brand-amber text-xs flex items-center justify-center font-bold">
              {idx + 1}
            </span>
            <p className="text-sm text-text-secondary leading-relaxed">{suggestion}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
