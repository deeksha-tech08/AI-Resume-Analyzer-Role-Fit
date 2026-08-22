/**
 * Full-page loading overlay with animated gradient spinner.
 */
import React from 'react';

export default function Loading({ message = 'Loading...' }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background-primary/80 backdrop-blur-sm">
      <div className="flex flex-col items-center gap-4 slide-up">
        {/* Animated gradient spinner */}
        <div className="relative w-16 h-16">
          <div className="absolute inset-0 rounded-full border-4 border-border-subtle" />
          <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-brand-primary border-r-brand-secondary animate-spin" />
        </div>
        <p className="text-text-secondary text-sm font-medium">{message}</p>
      </div>
    </div>
  );
}
