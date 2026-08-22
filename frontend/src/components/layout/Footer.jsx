/**
 * Footer component with copyright and links.
 */
import React from 'react';

export default function Footer() {
  return (
    <footer className="w-full mt-auto py-6 border-t border-border-subtle bg-background-secondary/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row justify-between items-center gap-3">
        <p className="text-text-secondary text-sm">
          &copy; {new Date().getFullYear()} AI Resume Analyzer &amp; Role Fit System
        </p>
        <div className="flex items-center gap-4">
          <a href="#" className="text-text-secondary hover:text-text-primary text-sm transition-colors">About</a>
          <span className="text-border-subtle">|</span>
          <a href="#" className="text-text-secondary hover:text-text-primary text-sm transition-colors">GitHub</a>
          <span className="text-border-subtle">|</span>
          <span className="text-text-secondary text-sm">Built with ❤️</span>
        </div>
      </div>
    </footer>
  );
}
