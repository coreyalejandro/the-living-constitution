import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {SiliconHill} from './components/SiliconHill';
import {TheBuild} from './components/TheBuild';
import {pillars} from './data/pillars';

const getActLabel = (frame: number): string => {
  if (frame < 180) return 'ACT I — THE CONCEPT';
  if (frame < 336) return 'ACT II — THE MECHANISM';
  if (frame < 576) return 'ACT III — THE 10 PILLARS';
  return 'ACT IV — THE RESOLUTION';
};

export const Video: React.FC = () => {
  const frame = useCurrentFrame();
  const seconds = frame / 12;
  const actLabel = getActLabel(frame);
  const inBridge = frame >= 336 && frame < 576;
  const pillarIndex = inBridge ? Math.min(9, Math.floor((frame - 336) / 24)) : 0;
  const verified = frame >= 150;

  return (
    <AbsoluteFill style={{backgroundColor: '#FEF9E7'}}>
      <svg width="1080" height="1080" viewBox="0 0 1080 1080">
        <SiliconHill />
        <TheBuild
          x={frame < 180 ? 90 : frame < 336 ? 180 + (frame - 180) * 2.2 : frame < 576 ? 500 : 760}
          y={frame < 180 ? 660 : frame < 336 ? 660 - (frame - 180) * 1.6 : frame < 576 ? 520 : 360}
          scale={1.2}
          verified={verified}
        />
      </svg>

      <div
        style={{
          position: 'absolute',
          top: 28,
          left: 28,
          padding: '10px 14px',
          backgroundColor: 'rgba(254, 249, 231, 0.9)',
          border: '4px solid #2D2D2D',
          fontFamily: 'Courier New, monospace',
          fontWeight: 700,
          fontSize: 28,
          color: '#2D2D2D',
        }}
      >
        {actLabel}
      </div>

      {frame < 180 ? (
        <div
          style={{
            position: 'absolute',
            left: 80,
            bottom: 80,
            width: 560,
            fontFamily: 'Courier New, monospace',
            fontSize: 34,
            lineHeight: 1.2,
            color: '#2D2D2D',
            backgroundColor: 'rgba(254, 249, 231, 0.88)',
            border: '4px solid #2D2D2D',
            padding: 20,
          }}
        >
          I'm just a Build. Yes, I'm only a Build.<br />
          And I'm sitting here on Silicon Hill.
        </div>
      ) : null}

      {inBridge ? (
        <div
          style={{
            position: 'absolute',
            top: 180,
            right: 70,
            width: 360,
            padding: 18,
            backgroundColor: 'rgba(45, 45, 45, 0.85)',
            color: '#FEF9E7',
            border: '4px solid #E1AD01',
            fontFamily: 'Courier New, monospace',
          }}
        >
          <div style={{fontSize: 22, marginBottom: 10}}>PILLAR {pillarIndex + 1}</div>
          <div style={{fontSize: 34, lineHeight: 1.1}}>{pillars[pillarIndex]}</div>
        </div>
      ) : null}

      {frame >= 576 ? (
        <div
          style={{
            position: 'absolute',
            right: 72,
            bottom: 140,
            padding: '18px 24px',
            backgroundColor: '#2E8B57',
            border: '5px solid #2D2D2D',
            color: '#FEF9E7',
            fontFamily: 'Courier New, monospace',
            fontSize: 38,
            fontWeight: 700,
          }}
        >
          VALIDATED
        </div>
      ) : null}

      <div
        style={{
          position: 'absolute',
          bottom: 14,
          right: 18,
          fontFamily: 'Courier New, monospace',
          fontSize: 12,
          color: '#2D2D2D',
        }}
      >
        DETERMINISTIC_RENDER | t={seconds.toFixed(2)}s
      </div>
    </AbsoluteFill>
  );
};
