import React from 'react';
import {useJitter} from '../hooks/useJitter';

type TheBuildProps = {
  x?: number;
  y?: number;
  scale?: number;
  verified?: boolean;
};

export const TheBuild: React.FC<TheBuildProps> = ({
  x = 100,
  y = 200,
  scale = 1,
  verified = false,
}) => {
  const jitter = useJitter();
  const sealFill = verified ? '#2E8B57' : '#CC5500';

  return (
    <g transform={`translate(${x} ${y}) scale(${scale})`} style={jitter}>
      <path d="M40 50 H160 V250 H40 Z" fill="#FEF9E7" stroke="#E1AD01" strokeWidth="8" />
      <ellipse cx="100" cy="50" rx="65" ry="15" fill="#FEF9E7" stroke="#E1AD01" strokeWidth="6" />
      <circle cx="100" cy="200" r="30" fill={sealFill} stroke="#8B0000" strokeWidth="4" />
      <path d="M85 200 L115 200 M100 185 L100 215" stroke="#FEF9E7" strokeWidth="3" strokeLinecap="round" />
      <circle cx="78" cy="130" r="5" fill="#2D2D2D" />
      <circle cx="122" cy="130" r="5" fill="#2D2D2D" />
      <path d="M82 158 Q100 168 118 158" stroke="#2D2D2D" strokeWidth="4" fill="none" strokeLinecap="round" />
    </g>
  );
};
