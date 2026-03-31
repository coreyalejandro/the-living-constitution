/**
 * Stepped interpolation for analog, non-glossy motion (no spring overshoot).
 */
export function stepToward(
  from: number,
  to: number,
  t: number,
  steps: number,
): number {
  const clamped = Math.min(1, Math.max(0, t));
  const s = Math.max(1, steps);
  const stepped = Math.floor(clamped * s) / s;
  return from + (to - from) * stepped;
}

export function clamp01(n: number): number {
  return Math.min(1, Math.max(0, n));
}
