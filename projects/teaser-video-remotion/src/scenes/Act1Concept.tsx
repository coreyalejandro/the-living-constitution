import React from 'react';
import {AbsoluteFill} from 'remotion';
import {BuildCharacter} from '../components/BuildCharacter';
import {palette} from '../lib/palette';
import {ACT1_START} from '../composition/VideoConfig';
import {stepToward} from '../lib/easing';

type Props = {
  frame: number;
};

export const Act1Concept: React.FC<Props> = ({frame}) => {
  const local = frame - ACT1_START;
  const t = Math.min(1, local / 120);
  const rise = stepToward(40, 0, t, 8);

  return (
    <AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          top: 120 + rise,
          left: 0,
          right: 0,
          display: 'flex',
          justifyContent: 'center',
        }}
      >
        <BuildCharacter frame={frame} mood="uncertain" scale={1.05} />
      </div>
      <div
        style={{
          position: 'absolute',
          top: 72,
          width: '100%',
          textAlign: 'center',
          fontFamily: 'Arial Black, sans-serif',
          fontSize: 28,
          color: palette.ink,
          letterSpacing: 1,
        }}
      >
        ACT I — CONCEPT
      </div>
    </AbsoluteFill>
  );
};
