import {useCurrentFrame} from 'remotion';

type JitterStyle = {
  transform: string;
};

const seededUnit = (seed: number): number => {
  return ((seed * 9301 + 49297) % 233280) / 233280;
};

export const useJitter = (): JitterStyle => {
  const frame = useCurrentFrame();

  if (frame % 2 !== 0) {
    return {transform: 'translate(0px, 0px)'};
  }

  const x = seededUnit(frame + 11) * 2 - 1;
  const y = seededUnit(frame + 29) * 2 - 1;

  return {
    transform: `translate(${x.toFixed(3)}px, ${y.toFixed(3)}px)`,
  };
};
