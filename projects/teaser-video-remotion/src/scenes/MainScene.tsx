import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Act1Concept} from './Act1Concept';
import {Act2Mechanism} from './Act2Mechanism';
import {Act3Pillars} from './Act3Pillars';
import {Act4Validation} from './Act4Validation';
import {ACT1_END, ACT2_END, ACT3_END} from '../composition/VideoConfig';

export const MainScene: React.FC = () => {
  const frame = useCurrentFrame();

  if (frame <= ACT1_END) {
    return <Act1Concept frame={frame} />;
  }

  if (frame <= ACT2_END) {
    return <Act2Mechanism frame={frame} />;
  }

  if (frame <= ACT3_END) {
    return <Act3Pillars frame={frame} />;
  }

  return <Act4Validation frame={frame} />;
};
