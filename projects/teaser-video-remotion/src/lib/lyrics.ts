export type CaptionLines = {
  line1: string;
  line2?: string;
};

/**
 * Authoritative caption lines per global frame (see LYRICS_TIMECODE.md).
 */
export function getCaptionForFrame(frame: number): CaptionLines | null {
  if (frame <= 47) {
    return {line1: "I'm just a build, yes, only a build"};
  }
  if (frame <= 95) {
    return {line1: "Up on Silicon Hill, but I'm not ready still"};
  }
  if (frame <= 143) {
    return {line1: 'I started as a maybe, a rough and risky draft'};
  }
  if (frame <= 179) {
    return {line1: 'No proof, no guardrails, no lawful path'};
  }
  if (frame <= 227) {
    return {line1: 'Then the Constitution drew a line'};
  }
  if (frame <= 275) {
    return {line1: 'With explicit rules and checks in time'};
  }
  if (frame <= 323) {
    return {line1: 'C-RSP said: one clear pass'};
  }
  if (frame <= 359) {
    return {line1: 'Show your proof, or you do not pass'};
  }
  if (frame <= 401) {
    return {
      line1: 'Scope and constraints, deterministic ways',
    };
  }
  if (frame <= 443) {
    return {
      line1: 'Powers divided, verification stays',
    };
  }
  if (frame <= 491) {
    return {
      line1: 'Truth with evidence, failures that halt',
    };
  }
  if (frame <= 539) {
    return {
      line1: 'Reproducible release is the final result',
    };
  }
  if (frame <= 599) {
    return {line1: "Now I'm a build with a lawful claim"};
  }
  if (frame <= 659) {
    return {line1: 'Verified, repeatable, not just a name'};
  }
  return {
    line1: "I'm just a build, but now you can see",
    line2: 'A governed release is what made me me',
  };
}
