const trustSurfaces = [
  {
    label: "Authoritative repository status",
    path: "STATUS.json",
    className: "canonical",
    machineEnforced: true,
    note: "Current machine-readable status anchor.",
  },
  {
    label: "Architecture guide",
    path: "PROGRAM_ARCHITECTURE.md",
    className: "narrative",
    machineEnforced: false,
    note: "Describes layers and trust boundaries.",
  },
  {
    label: "Derived module summary",
    path: "MODULE_STATUS.md",
    className: "derived",
    machineEnforced: false,
    note: "Orientation surface; verify against cited sources.",
  },
  {
    label: "Trust surface guide",
    path: "docs/governance/TRUST_SURFACE_GUIDE.md",
    className: "canonical",
    machineEnforced: false,
    note: "Explains how to read canonical, narrative, and derived artifacts.",
  },
];

const notClaimed = [
  "Tier-1 equivalence is achieved",
  "Production readiness is established",
  "Accessibility compliance certification exists",
  "Empirical validation of cognitive-mode effectiveness is complete",
];

const menuOptions = [
  "Show repository status",
  "Explain trust surfaces",
  "List what is not claimed",
  "Exit",
];

module.exports = {
  trustSurfaces,
  notClaimed,
  menuOptions,
};
