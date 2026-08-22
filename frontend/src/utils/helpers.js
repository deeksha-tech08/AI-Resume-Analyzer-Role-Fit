/**
 * Utility helpers for formatting and display.
 */

export function getScoreColor(score) {
  if (score >= 75) return 'text-brand-emerald';
  if (score >= 55) return 'text-brand-cyan';
  if (score >= 35) return 'text-brand-amber';
  return 'text-brand-rose';
}

export function getScoreLabel(score) {
  if (score >= 75) return 'Strong';
  if (score >= 55) return 'Good';
  if (score >= 35) return 'Average';
  return 'Weak';
}

export function getScoreBg(score) {
  if (score >= 75) return 'strong';
  if (score >= 55) return 'good';
  if (score >= 35) return 'average';
  return 'weak';
}

export function formatDate(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
  });
}

export function formatDateTime(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

export function truncate(str, maxLen = 50) {
  if (!str) return '';
  return str.length > maxLen ? str.slice(0, maxLen) + '...' : str;
}
