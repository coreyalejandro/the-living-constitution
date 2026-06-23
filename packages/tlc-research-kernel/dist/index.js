"use strict";
/**
 * index.ts — tlc-research-kernel barrel export
 *
 * TLC Research Workbench kernel package.
 * Provides typed interfaces and utilities for surfacing CGL experiment data
 * in the TLC control plane without blurring the TLC/CGL boundary.
 *
 * TLC governs the arc. CGL runs the experiment.
 * See: research/TLC-CGL-BOUNDARY.md
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
__exportStar(require("./experiment-schema"), exports);
__exportStar(require("./eval-runner"), exports);
__exportStar(require("./constitutional-critic"), exports);
__exportStar(require("./improvement-proposer"), exports);
__exportStar(require("./regression-gate"), exports);
__exportStar(require("./provenance"), exports);
//# sourceMappingURL=index.js.map