import React from 'react';
import {AbsoluteFill} from 'remotion';
import {palette} from '../lib/palette';

export const KimiScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: palette.offWhite,
        color: palette.ink,
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: 'Arial Black, sans-serif',
        textAlign: 'center',
        padding: 48,
      }}
    >
      <h1 style={{fontSize: 52, margin: 0}}>Kimi Remix</h1>
      <p style={{fontSize: 26, maxWidth: 760, fontFamily: 'Georgia, serif'}}>
        Placeholder scene kept for side-by-side versioning in Remotion Studio.
      </p>
    </AbsoluteFill>
  );
};
