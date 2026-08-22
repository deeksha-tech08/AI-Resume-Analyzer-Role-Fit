/**
 * RoleCard — displays a single role's fit score, core coverage, and skill breakdown.
 */
import React from 'react';
import FitScoreRing from './FitScoreRing';
import SkillList from './SkillList';

export default function RoleCard({ roleScore, isBestFit = false, rank = null }) {
  const { role, fit_score, core_skill_coverage, matched_skills, missing_core_skills, missing_optional_skills } = roleScore;

  const getRankBadge = () => {
    if (rank === 1) return <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-brand-primary/20 text-brand-primary">🏆 #1 Best Match</span>;
    if (rank === 2) return <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-gray-300/20 text-gray-300">🥈 #2 Match</span>;
    if (rank === 3) return <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-yellow-600/20 text-yellow-600">🥉 #3 Match</span>;
    if (rank) return <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-white/10 text-white">#{rank} Match</span>;
    if (isBestFit) return <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-brand-primary/20 text-brand-primary">⭐ Best Fit</span>;
    return null;
  };

  return (
    <div className={`glass-card p-6 slide-up ${isBestFit || rank === 1 ? 'best-fit-glow' : ''}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <div className="flex flex-wrap items-center gap-2">
            <h3 className="text-lg font-semibold text-text-primary">{role}</h3>
            {getRankBadge()}
          </div>
          <p className="text-sm text-text-secondary mt-1">
            Core Coverage: {core_skill_coverage}%
          </p>
        </div>
        <FitScoreRing score={fit_score} size={80} label="Fit" />
      </div>

      {/* Core Coverage Bar */}
      <div className="mb-4">
        <div className="flex justify-between text-xs text-text-secondary mb-1">
          <span>Core Skill Coverage</span>
          <span>{core_skill_coverage}%</span>
        </div>
        <div className="progress-bar">
          <div
            className={`progress-bar-fill ${core_skill_coverage >= 75 ? 'strong' : core_skill_coverage >= 50 ? 'good' : core_skill_coverage >= 25 ? 'average' : 'weak'}`}
            style={{ width: `${core_skill_coverage}%` }}
          />
        </div>
      </div>

      {/* Skills Breakdown */}
      <SkillList
        matched={matched_skills}
        missingCore={missing_core_skills}
        missingOptional={missing_optional_skills}
      />
    </div>
  );
}
