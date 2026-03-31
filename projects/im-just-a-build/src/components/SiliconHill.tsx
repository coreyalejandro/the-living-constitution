import React from 'react';
import {useJitter} from '../hooks/useJitter';

export const SiliconHill: React.FC = () => {
  const jitter = useJitter();

  return (
    <g style={jitter}>
      <defs>
        <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#E1AD01" stopOpacity="1" />
          <stop offset="100%" stopColor="#FEF9E7" stopOpacity="1" />
        </linearGradient>
      </defs>
      <rect width="1080" height="1080" fill="url(#skyGrad)" />
      <path d="M180 200 L840 200 L880 940 L140 940 Z" fill="#4B5320" stroke="#2D2D2D" strokeWidth="10" strokeLinecap="round" />
      <path d="M175 300 H845 M170 420 H850 M165 540 H855 M160 660 H860 M155 780 H865" stroke="#E1AD01" strokeWidth="6" strokeDasharray="10 15" strokeLinecap="round" />
      <rect x="360" y="95" width="320" height="95" rx="18" fill="#CC5500" stroke="#2D2D2D" strokeWidth="5" />
      <text x="520" y="153" textAnchor="middle" fontFamily="Courier New, monospace" fontSize="36" fontWeight="700" fill="#FEF9E7">
        SILICON HILL
      </text>
    </g>
  );
};
