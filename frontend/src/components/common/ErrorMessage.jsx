/**
 * Error message display with optional retry button.
 */
import React from 'react';
import Button from './Button';

export default function ErrorMessage({ message = 'Something went wrong', onRetry = null }) {
  return (
    <div className="glass-card border-brand-rose/30 p-6 text-center max-w-md mx-auto slide-up">
      <div className="flex justify-center mb-3">
        <div className="w-12 h-12 rounded-full bg-brand-rose/10 flex items-center justify-center">
          <svg className="w-6 h-6 text-brand-rose" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        </div>
      </div>
      <p className="text-text-primary font-medium mb-1">Error</p>
      <p className="text-text-secondary text-sm mb-4">{message}</p>
      {onRetry && (
        <Button variant="secondary" size="sm" onClick={onRetry}>
          Try Again
        </Button>
      )}
    </div>
  );
}
