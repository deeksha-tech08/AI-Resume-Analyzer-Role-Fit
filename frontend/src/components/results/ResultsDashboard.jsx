/**
 * ResultsDashboard — main container assembling all analysis result components.
 */
import React from 'react';
import BestFitHighlight from './BestFitHighlight';
import WhyThisScore from './WhyThisScore';
import SectionAnalysis from './SectionAnalysis';
import RoleCard from '../analysis/RoleCard';
import SuggestionCard from '../analysis/SuggestionCard';

export default function ResultsDashboard({ analysis }) {
  if (!analysis) return null;

  const { role_scores, best_fit_role, ats_score, explanation, suggestions, section_strength, selected_roles } = analysis;
  const bestRole = role_scores?.find(r => r.role === best_fit_role) || role_scores?.[0];

  return (
    <div className="space-y-6 max-w-4xl mx-auto w-full">
      {/* Best Fit Highlight */}
      <BestFitHighlight bestRole={bestRole} atsScore={ats_score} />

      {/* AI Explanation */}
      <WhyThisScore explanation={explanation} />

      {/* All Role Scores */}
      <div>
        <h3 className="text-lg font-semibold text-text-primary mb-4">
          {selected_roles?.length > 4 ? "Your Top 5 Role Matches" : "Role Fit Scores"}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {role_scores?.slice(0, selected_roles?.length > 4 ? 5 : undefined).map((rs, idx) => (
            <RoleCard
              key={rs.role}
              roleScore={rs}
              isBestFit={rs.role === best_fit_role}
              rank={selected_roles?.length > 4 ? idx + 1 : null}
            />
          ))}
        </div>
      </div>

      {/* AI Suggestions */}
      <SuggestionCard suggestions={suggestions} />

      {/* Section Strength Analysis */}
      <SectionAnalysis sections={section_strength} />
    </div>
  );
}
