import React from 'react';
import {AbsoluteFill} from 'remotion';
import {palette} from '../lib/palette';

export const OldSchoolScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: palette.cream,
        color: palette.ink,
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: 'Georgia, serif',
        textAlign: 'center',
        padding: 48,
      }}
    >
      <h1 style={{fontSize: 56, margin: 0}}>Old School Build</h1>
      <p style={{fontSize: 28, maxWidth: 760}}>
        Legacy flat version preserved as a compatibility composition.
      </p>
    </AbsoluteFill>
  );
};
