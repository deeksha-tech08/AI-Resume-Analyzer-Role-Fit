/**
 * BestFitHighlight — prominent display of the best-fit role.
 */
import React from 'react';
import FitScoreRing from '../analysis/FitScoreRing';

export default function BestFitHighlight({ bestRole, atsScore }) {
  if (!bestRole) return null;

  return (
    <div className="glass-card best-fit-glow p-8 text-center slide-up">
      <p className="text-sm text-text-secondary uppercase tracking-wider mb-2">Best Fit Role</p>
      <h2 className="text-3xl font-bold gradient-text mb-4">{bestRole.role}</h2>
      <div className="flex items-center justify-center gap-8">
        <FitScoreRing score={bestRole.fit_score} size={120} label="Role Fit" />
        <FitScoreRing score={atsScore} size={120} label="ATS Score" />
      </div>
      <p className="text-text-secondary text-sm mt-4">
        Core Skill Coverage: <span className="text-text-primary font-semibold">{bestRole.core_skill_coverage}%</span>
      </p>
    </div>
  );
}
