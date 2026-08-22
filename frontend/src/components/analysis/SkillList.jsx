/**
 * SkillList — displays matched, missing core, and missing optional skills.
 */
import React, { useState } from 'react';

export default function SkillList({ matched = [], missingCore = [], missingOptional = [] }) {
  const [expanded, setExpanded] = useState(false);

  const totalSkills = matched.length + missingCore.length + missingOptional.length;
  const showToggle = totalSkills > 6;
  const visibleLimit = expanded ? totalSkills : 6;

  const allSkills = [
    ...matched.map(s => ({ name: s, type: 'matched' })),
    ...missingCore.map(s => ({ name: s, type: 'missing-core' })),
    ...missingOptional.map(s => ({ name: s, type: 'missing-optional' })),
  ];

  return (
    <div>
      <div className="flex flex-wrap gap-2">
        {allSkills.slice(0, visibleLimit).map((skill) => (
          <span key={skill.name} className={`skill-tag ${skill.type}`}>
            {skill.type === 'matched' && '✓ '}
            {skill.type === 'missing-core' && '✗ '}
            {skill.type === 'missing-optional' && '~ '}
            {skill.name}
          </span>
        ))}
      </div>
      {showToggle && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-xs text-brand-primary hover:text-brand-secondary mt-2 transition-colors"
        >
          {expanded ? 'Show less' : `+${totalSkills - 6} more skills`}
        </button>
      )}
      {/* Legend */}
      <div className="flex gap-4 mt-3 text-xs text-text-secondary">
        <span>✓ Matched</span>
        <span>✗ Missing Core</span>
        <span>~ Optional</span>
      </div>
    </div>
  );
}
