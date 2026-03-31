import React from 'react';
import {palette} from '../lib/palette';
import {seededScalar} from '../lib/deterministic';

type Props = {
  frame: number;
  variant?: 'dawn' | 'mechanism' | 'grid' | 'clear';
};

export const SiliconHill: React.FC<Props> = ({frame, variant = 'dawn'}) => {
  const drift = seededScalar('hill-drift', frame, variant === 'mechanism' ? 6 : 3);

  const sky =
    variant === 'clear'
      ? palette.offWhite
      : variant === 'mechanism'
        ? palette.mustard
        : variant === 'grid'
          ? palette.cream
          : palette.olive;

  return (
    <svg
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        transform: `translateX(${drift}px)`,
      }}
      viewBox="0 0 1080 1080"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden
    >
      <rect width="1080" height="1080" fill={sky} />
      <path
        d="M0 620 Q 180 520 360 580 T 720 560 T 1080 600 L 1080 1080 L 0 1080 Z"
        fill={palette.olive}
        stroke={palette.ink}
        strokeWidth="4"
      />
      <path
        d="M0 680 Q 220 600 440 640 T 880 620 L 1080 640 L 1080 1080 L 0 1080 Z"
        fill={palette.burntOrange}
        stroke={palette.ink}
        strokeWidth="3"
        opacity={0.85}
      />
      {rackBlocks(frame, 120, 640)}
      {rackBlocks(frame, 380, 620)}
      {rackBlocks(frame, 640, 650)}
      {variant === 'mechanism' ? (
        <rect
          x="80"
          y="120"
          width="920"
          height="8"
          fill={palette.ink}
          opacity={0.15}
        />
      ) : null}
    </svg>
  );
};

function rackBlocks(frame: number, baseX: number, baseY: number) {
  const blocks: React.ReactNode[] = [];
  for (let i = 0; i < 5; i++) {
    const bx = baseX + i * 34;
    const jitter = seededScalar(`rack-${baseX}-${i}`, frame, 1.5);
    blocks.push(
      <rect
        key={`${baseX}-${i}`}
        x={bx + jitter}
        y={baseY - i * 8}
        width="28"
        height="72"
        fill={palette.mustard}
        stroke={palette.ink}
        strokeWidth="3"
      />,
    );
    blocks.push(
      <line
        key={`${baseX}-${i}-l`}
        x1={bx + 4 + jitter}
        y1={baseY + 20 - i * 8}
        x2={bx + 24 + jitter}
        y2={baseY + 20 - i * 8}
        stroke={palette.ink}
        strokeWidth="2"
      />,
    );
  }
  return blocks;
}
