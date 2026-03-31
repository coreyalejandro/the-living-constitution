import React from 'react';
import {AbsoluteFill} from 'remotion';
import {BuildCharacter} from '../components/BuildCharacter';
import {palette} from '../lib/palette';
import {ACT2_START} from '../composition/VideoConfig';
import {stepToward} from '../lib/easing';

type Props = {
  frame: number;
};

export const Act2Mechanism: React.FC<Props> = ({frame}) => {
  const local = frame - ACT2_START;
  const t = Math.min(1, local / 140);
  const slide = stepToward(-80, 0, t, 10);

  return (
    <AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          top: 96,
          width: '100%',
          textAlign: 'center',
          fontFamily: 'Arial Black, sans-serif',
          fontSize: 28,
          color: palette.ink,
        }}
      >
        ACT II — MECHANISM
      </div>
      <svg
        style={{position: 'absolute', inset: 0, width: '100%', height: '100%'}}
        viewBox="0 0 1080 1080"
        aria-hidden
      >
        <rect
          x="120"
          y="320"
          width="320"
          height="200"
          fill="none"
          stroke={palette.ink}
          strokeWidth="5"
          strokeDasharray="14 10"
          transform={`translate(${slide}, 0)`}
        />
        <path
          d="M 460 420 L 620 420"
          stroke={palette.ink}
          strokeWidth="6"
          markerEnd="url(#arrowhead)"
        />
        <defs>
          <marker
            id="arrowhead"
            markerWidth="12"
            markerHeight="12"
            refX="10"
            refY="6"
            orient="auto"
          >
            <path d="M0,0 L12,6 L0,12 z" fill={palette.ink} />
          </marker>
        </defs>
        <rect
          x="640"
          y="300"
          width="300"
          height="240"
          fill={palette.offWhite}
          stroke={palette.ink}
          strokeWidth="5"
        />
        <text
          x="790"
          y="380"
          textAnchor="middle"
          fill={palette.ink}
          fontFamily="Georgia, serif"
          fontSize="22"
          fontWeight="bold"
        >
          C-RSP
        </text>
        <text
          x="790"
          y="420"
          textAnchor="middle"
          fill={palette.ink}
          fontFamily="Georgia, serif"
          fontSize="18"
        >
          Single pass
        </text>
        <text
          x="790"
          y="455"
          textAnchor="middle"
          fill={palette.ink}
          fontFamily="Georgia, serif"
          fontSize="18"
        >
          Proof gate
        </text>
      </svg>
      <div
        style={{
          position: 'absolute',
          bottom: 220,
          left: 0,
          right: 0,
          display: 'flex',
          justifyContent: 'center',
        }}
      >
        <BuildCharacter frame={frame} mood="regulated" scale={0.92} />
      </div>
    </AbsoluteFill>
  );
};
