import React from 'react';
import {palette} from '../lib/palette';
import {seededJitter, seededScalar} from '../lib/deterministic';

type Props = {
  frame: number;
  mood: 'uncertain' | 'regulated' | 'verified';
  scale?: number;
};

export const BuildCharacter: React.FC<Props> = ({frame, mood, scale = 1}) => {
  const wobble = seededJitter('build-body', frame, mood === 'uncertain' ? 4 : 2);
  const rot = seededScalar('build-tilt', frame, mood === 'uncertain' ? 2.5 : 1);

  return (
    <div
      style={{
        transform: `translate(${wobble.x}px, ${wobble.y}px) rotate(${rot}deg) scale(${scale})`,
        transformOrigin: 'center center',
      }}
    >
      <svg
        width={220}
        height={280}
        viewBox="0 0 220 280"
        aria-hidden
      >
        <rect
          x="8"
          y="8"
          width="204"
          height="264"
          rx="12"
          fill={palette.offWhite}
          stroke={palette.ink}
          strokeWidth="6"
        />
        <line
          x1="32"
          y1="48"
          x2="188"
          y2="48"
          stroke={palette.ink}
          strokeWidth="3"
        />
        <line
          x1="32"
          y1="68"
          x2="160"
          y2="68"
          stroke={palette.ink}
          strokeWidth="2"
        />
        <line
          x1="32"
          y1="84"
          x2="176"
          y2="84"
          stroke={palette.ink}
          strokeWidth="2"
        />
        <text
          x="110"
          y="130"
          textAnchor="middle"
          fill={palette.ink}
          fontFamily="Georgia, serif"
          fontSize="14"
          fontWeight="bold"
        >
          BUILD CONTRACT
        </text>
        <circle cx="92" cy="158" r="10" fill={palette.ink} />
        <circle cx="128" cy="158" r="10" fill={palette.ink} />
        <path
          d="M 88 182 Q 110 198 132 182"
          fill="none"
          stroke={palette.ink}
          strokeWidth="4"
          strokeLinecap="round"
        />
        <ellipse
          cx="158"
          cy="210"
          rx="28"
          ry="20"
          fill={palette.waxRed}
          stroke={palette.ink}
          strokeWidth="4"
        />
        <text
          x="158"
          y="216"
          textAnchor="middle"
          fill={palette.offWhite}
          fontFamily="Arial Black, sans-serif"
          fontSize="11"
        >
          C
        </text>
        {mood === 'verified' ? (
          <rect
            x="36"
            y="228"
            width="148"
            height="28"
            fill={palette.mustard}
            stroke={palette.ink}
            strokeWidth="3"
          />
        ) : null}
        {mood === 'verified' ? (
          <text
            x="110"
            y="248"
            textAnchor="middle"
            fill={palette.ink}
            fontFamily="Arial Black, sans-serif"
            fontSize="14"
          >
            VERIFIED
          </text>
        ) : null}
      </svg>
    </div>
  );
};
