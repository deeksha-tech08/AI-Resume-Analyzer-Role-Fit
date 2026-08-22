/**
 * SectionStrengthCard — displays section-level strength analysis.
 */
import React from 'react';
import { getScoreBg } from '../../utils/helpers';

export default function SectionStrengthCard({ sections = [] }) {
  if (!sections.length) return null;

  const labelColors = {
    Strong: 'badge-strong',
    Good: 'badge-good',
    Average: 'badge-average',
    Weak: 'badge-weak',
  };

  return (
    <div className="glass-card p-6 slide-up">
      <h3 className="text-lg font-semibold text-text-primary mb-4 flex items-center gap-2">
        <svg className="w-5 h-5 text-brand-cyan" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" />
        </svg>
        Section Strength Analysis
      </h3>
      <div className="space-y-4">
        {sections.map((section) => (
          <div key={section.section} className="p-3 rounded-lg bg-white/[0.02] border border-border-subtle">
            <div className="flex items-center justify-between mb-2">
              <span className="font-medium text-text-primary">{section.section}</span>
              <div className="flex items-center gap-2">
                <span className={labelColors[section.label] || 'badge-average'}>{section.label}</span>
                <span className="text-sm font-semibold text-text-secondary">{section.score}%</span>
              </div>
            </div>
            <div className="progress-bar mb-2">
              <div
                className={`progress-bar-fill ${getScoreBg(section.score)}`}
                style={{ width: `${section.score}%` }}
              />
            </div>
            {section.detected_strengths?.length > 0 && (
              <div className="flex flex-wrap gap-1.5 mb-1.5">
                {section.detected_strengths.map((s, i) => (
                  <span key={i} className="text-xs text-brand-emerald bg-brand-emerald/10 px-2 py-0.5 rounded">
                    ✓ {s}
                  </span>
                ))}
              </div>
            )}
            {section.tip && (
              <p className="text-xs text-brand-amber mt-1">💡 {section.tip}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
