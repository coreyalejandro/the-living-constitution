import React from 'react';
import {palette} from '../lib/palette';
import {seededJitter} from '../lib/deterministic';

type Props = {
  line1: string;
  line2?: string;
  frame: number;
};

export const CaptionCard: React.FC<Props> = ({line1, line2, frame}) => {
  const nudge = seededJitter('caption', frame, 1);

  return (
    <div
      style={{
        position: 'absolute',
        left: 48 + nudge.x,
        right: 48 + nudge.x,
        bottom: 40 + nudge.y,
        padding: '18px 22px',
        backgroundColor: palette.offWhite,
        border: `5px solid ${palette.ink}`,
        borderRadius: 4,
        boxShadow: '6px 6px 0 rgba(26,26,26,0.12)',
      }}
    >
      <div
        style={{
          fontFamily: 'Arial Black, Helvetica, sans-serif',
          fontSize: line2 ? 30 : 34,
          lineHeight: 1.25,
          color: palette.ink,
          textAlign: 'center',
          textTransform: 'none',
        }}
      >
        {line1}
      </div>
      {line2 ? (
        <div
          style={{
            marginTop: 10,
            fontFamily: 'Georgia, Times New Roman, serif',
            fontSize: 28,
            lineHeight: 1.2,
            color: palette.ink,
            textAlign: 'center',
            fontWeight: 700,
          }}
        >
          {line2}
        </div>
      ) : null}
    </div>
  );
};
