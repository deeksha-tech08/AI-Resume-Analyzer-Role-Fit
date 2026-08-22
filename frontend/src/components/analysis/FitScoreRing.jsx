/**
 * FitScoreRing — circular score visualization using Recharts PieChart.
 */
import React from 'react';
import { PieChart, Pie, Cell } from 'recharts';
import { getScoreColor } from '../../utils/helpers';

export default function FitScoreRing({ score, size = 120, label = '' }) {
  const data = [
    { value: score },
    { value: 100 - score },
  ];

  const colorVar = score >= 75 ? '#10b981' : score >= 55 ? '#06b6d4' : score >= 35 ? '#f59e0b' : '#f43f5e';
  const bgColor = 'rgba(255,255,255,0.05)';

  return (
    <div className="score-ring" style={{ width: size, height: size }}>
      <PieChart width={size} height={size}>
        <Pie
          data={data}
          cx={size / 2}
          cy={size / 2}
          innerRadius={size * 0.35}
          outerRadius={size * 0.45}
          startAngle={90}
          endAngle={-270}
          dataKey="value"
          stroke="none"
        >
          <Cell fill={colorVar} />
          <Cell fill={bgColor} />
        </Pie>
      </PieChart>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className={`text-xl font-bold ${getScoreColor(score)}`}>{score}%</span>
        {label && <span className="text-xs text-text-secondary mt-0.5">{label}</span>}
      </div>
    </div>
  );
}
