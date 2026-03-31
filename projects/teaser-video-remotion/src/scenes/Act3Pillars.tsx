import React from 'react';
import {AbsoluteFill} from 'remotion';
import {PillarGrid} from '../components/PillarGrid';
import {palette} from '../lib/palette';

type Props = {
  frame: number;
};

export const Act3Pillars: React.FC<Props> = ({frame}) => {
  return (
    <AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          top: 56,
          width: '100%',
          textAlign: 'center',
          fontFamily: 'Arial Black, sans-serif',
          fontSize: 28,
          color: palette.ink,
        }}
      >
        ACT III — 10 PILLARS
      </div>
      <PillarGrid frame={frame} />
    </AbsoluteFill>
  );
};
