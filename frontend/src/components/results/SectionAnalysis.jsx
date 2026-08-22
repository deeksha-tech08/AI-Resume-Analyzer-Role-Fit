/**
 * SectionAnalysis — wrapper for SectionStrengthCard (re-export for results layout).
 */
import React from 'react';
import SectionStrengthCard from '../analysis/SectionStrengthCard';

export default function SectionAnalysis({ sections }) {
  return <SectionStrengthCard sections={sections} />;
}
