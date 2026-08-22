/**
 * WhyThisScore — displays the AI-generated explanation.
 */
import React from 'react';

export default function WhyThisScore({ explanation }) {
  if (!explanation) return null;

  return (
    <div className="glass-card p-6 slide-up">
      <h3 className="text-lg font-semibold text-text-primary mb-3 flex items-center gap-2">
        <svg className="w-5 h-5 text-brand-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
        </svg>
        Why This Score?
      </h3>
      <p className="text-text-secondary leading-relaxed text-sm">{explanation}</p>
    </div>
  );
}
