import React from 'react';
import {AbsoluteFill} from 'remotion';
import {palette} from '../lib/palette';

export const VeoScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: palette.olive,
        color: palette.offWhite,
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: 'Arial Black, sans-serif',
        textAlign: 'center',
        padding: 48,
      }}
    >
      <h1 style={{fontSize: 52, margin: 0}}>Veo Cinematic</h1>
      <p style={{fontSize: 26, maxWidth: 800, fontFamily: 'Georgia, serif'}}>
        Placeholder composition for high-end cinematic comparison.
      </p>
    </AbsoluteFill>
  );
};
