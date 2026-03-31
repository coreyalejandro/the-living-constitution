import React from 'react';
import {PILLARS} from '../lib/pillars';
import {palette} from '../lib/palette';
import {stepToward} from '../lib/easing';
import {ACT3_START} from '../composition/VideoConfig';

type Props = {
  frame: number;
};

export const PillarGrid: React.FC<Props> = ({frame}) => {
  const local = frame - ACT3_START;
  const span = 180;
  const t = Math.min(1, Math.max(0, local / span));

  return (
    <div
      style={{
        position: 'absolute',
        left: 40,
        right: 40,
        top: 120,
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: 14,
      }}
    >
      {PILLARS.map((label, i) => {
        const stagger = i / PILLARS.length;
        const opacity = stepToward(0, 1, Math.min(1, (t - stagger * 0.4) / 0.6), 6);
        const highlight = local > i * 16;
        return (
          <div
            key={label}
            style={{
              opacity,
              padding: '12px 14px',
              backgroundColor: highlight ? palette.mustard : palette.offWhite,
              border: `4px solid ${palette.ink}`,
              borderRadius: 4,
              fontFamily: 'Arial Black, sans-serif',
              fontSize: 22,
              color: palette.ink,
              textAlign: 'left',
              lineHeight: 1.15,
            }}
          >
            <span style={{marginRight: 8}}>{i + 1}.</span>
            {label}
          </div>
        );
      })}
    </div>
  );
};
