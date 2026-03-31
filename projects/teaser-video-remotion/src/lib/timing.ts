import {
  ACT1_END,
  ACT1_START,
  ACT2_END,
  ACT2_START,
  ACT3_END,
  ACT3_START,
  ACT4_END,
  ACT4_START,
} from '../composition/VideoConfig';

export const acts = {
  act1: {label: 'Concept' as const, start: ACT1_START, end: ACT1_END},
  act2: {label: 'Mechanism' as const, start: ACT2_START, end: ACT2_END},
  act3: {label: '10 Pillars' as const, start: ACT3_START, end: ACT3_END},
  act4: {label: 'Validation / Resolution' as const, start: ACT4_START, end: ACT4_END},
} as const;

export function actIndexForFrame(frame: number): 1 | 2 | 3 | 4 {
  if (frame <= ACT1_END) {
    return 1;
  }
  if (frame <= ACT2_END) {
    return 2;
  }
  if (frame <= ACT3_END) {
    return 3;
  }
  return 4;
}

export function localFrameInAct(frame: number): {act: 1 | 2 | 3 | 4; local: number} {
  const a = actIndexForFrame(frame);
  const starts = [ACT1_START, ACT2_START, ACT3_START, ACT4_START] as const;
  return {act: a, local: frame - starts[a - 1]};
}
