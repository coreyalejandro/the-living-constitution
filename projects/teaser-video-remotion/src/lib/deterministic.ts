/**
 * Frame- and key-seeded jitter. No non-deterministic RNG, no wall-clock entropy.
 */

const FNV_OFFSET = 2166136261;
const FNV_PRIME = 16777619;

function fnv1a32(input: string): number {
  let hash = FNV_OFFSET;
  for (let i = 0; i < input.length; i++) {
    hash ^= input.charCodeAt(i);
    hash = Math.imul(hash, FNV_PRIME);
  }
  return hash >>> 0;
}

export function hashString(s: string): number {
  return fnv1a32(s);
}

/**
 * Returns a stable float in [0, 1) from semantic key and frame.
 */
export function unitFromKeyFrame(key: string, frame: number, salt = 0): number {
  const h = fnv1a32(`${key}\0${frame}\0${salt}`);
  return h / 0xffffffff;
}

/**
 * Seeded 2D offset; amplitude scales both axes symmetrically.
 */
export function seededJitter(
  key: string,
  frame: number,
  amplitude = 1,
): {x: number; y: number} {
  const ux = unitFromKeyFrame(key, frame, 0);
  const uy = unitFromKeyFrame(key, frame, 1);
  return {
    x: (ux * 2 - 1) * amplitude,
    y: (uy * 2 - 1) * amplitude,
  };
}

/**
 * Single scalar wobble in [-amplitude, amplitude].
 */
export function seededScalar(key: string, frame: number, amplitude = 1): number {
  const u = unitFromKeyFrame(key, frame, 2);
  return (u * 2 - 1) * amplitude;
}
