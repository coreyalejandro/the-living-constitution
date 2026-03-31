import React from 'react';
import {AbsoluteFill} from 'remotion';
import {BuildCharacter} from '../components/BuildCharacter';
import {palette} from '../lib/palette';
import {ACT4_START} from '../composition/VideoConfig';
import {stepToward} from '../lib/easing';

type Props = {
  frame: number;
};

export const Act4Validation: React.FC<Props> = ({frame}) => {
  const local = frame - ACT4_START;
  const t = Math.min(1, local / 100);
  const scale = stepToward(0.88, 1, t, 6);

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
        ACT IV — VALIDATION
      </div>
      <div
        style={{
          position: 'absolute',
          top: 200,
          left: 0,
          right: 0,
          display: 'flex',
          justifyContent: 'center',
        }}
      >
        <BuildCharacter frame={frame} mood="verified" scale={scale} />
      </div>
      <div
        style={{
          position: 'absolute',
          top: 520,
          left: 80,
          right: 80,
          padding: 16,
          backgroundColor: palette.olive,
          border: `4px solid ${palette.ink}`,
          fontFamily: 'Georgia, serif',
          fontSize: 24,
          color: palette.offWhite,
          textAlign: 'center',
          lineHeight: 1.3,
        }}
      >
        Uncertainty to regulation to proof to legitimacy — a governed release.
      </div>
    </AbsoluteFill>
  );
};
