import React from 'react';
import {AbsoluteFill, Composition, useCurrentFrame} from 'remotion';
import {
  ACT1_END,
  ACT2_END,
  ACT3_END,
  VIDEO_DURATION_FRAMES,
  VIDEO_FPS,
  VIDEO_HEIGHT,
  VIDEO_WIDTH,
} from './composition/VideoConfig';
import {Act1Concept} from './scenes/Act1Concept';
import {Act2Mechanism} from './scenes/Act2Mechanism';
import {Act3Pillars} from './scenes/Act3Pillars';
import {Act4Validation} from './scenes/Act4Validation';
import {CaptionCard} from './components/CaptionCard';
import {SiliconHill} from './components/SiliconHill';
import {getCaptionForFrame} from './lib/lyrics';
import {palette} from './lib/palette';

const ImJustABuild: React.FC = () => {
  const frame = useCurrentFrame();
  const caption = getCaptionForFrame(frame);

  let hill: 'dawn' | 'mechanism' | 'grid' | 'clear' = 'dawn';
  if (frame <= ACT1_END) {
    hill = 'dawn';
  } else if (frame <= ACT2_END) {
    hill = 'mechanism';
  } else if (frame <= ACT3_END) {
    hill = 'grid';
  } else {
    hill = 'clear';
  }

  return (
    <AbsoluteFill style={{backgroundColor: palette.cream}}>
      <SiliconHill frame={frame} variant={hill} />
      {frame <= ACT1_END ? <Act1Concept frame={frame} /> : null}
      {frame > ACT1_END && frame <= ACT2_END ? (
        <Act2Mechanism frame={frame} />
      ) : null}
      {frame > ACT2_END && frame <= ACT3_END ? (
        <Act3Pillars frame={frame} />
      ) : null}
      {frame > ACT3_END ? <Act4Validation frame={frame} /> : null}
      {caption ? (
        <CaptionCard
          line1={caption.line1}
          line2={caption.line2}
          frame={frame}
        />
      ) : null}
    </AbsoluteFill>
  );
};

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="ImJustABuild"
        component={ImJustABuild}
        durationInFrames={VIDEO_DURATION_FRAMES}
        fps={VIDEO_FPS}
        width={VIDEO_WIDTH}
        height={VIDEO_HEIGHT}
      />
    </>
  );
};
