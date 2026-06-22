#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const readline = require("readline");
const {
  trustSurfaces,
  notClaimed,
  menuOptions,
} = require("../interfaces/research-enablement");

const repoRoot = path.resolve(__dirname, "../..");

function readStatus() {
  try {
    const raw = fs.readFileSync(path.join(repoRoot, "STATUS.json"), "utf8");
    return JSON.parse(raw);
  } catch (error) {
    return {
      project: "unknown",
      status: "unavailable",
      reviewer_status: "unavailable",
      tip_state_truth: "unavailable",
      note: `Could not read STATUS.json: ${error.message}`,
    };
  }
}

function line(text = "") {
  process.stdout.write(`${text}\n`);
}

function renderHeader() {
  line("TLC Research Enablement TUI");
  line("Plain-English repository status and trust-surface guide");
  line("");
}

function renderStatus(status) {
  line("Repository status");
  line(`- Project: ${status.project ?? "unknown"}`);
  line(`- Current status: ${status.status ?? "unknown"}`);
  line(`- Reviewer status: ${status.reviewer_status ?? "unknown"}`);
  line(`- Truth at the tip: ${status.tip_state_truth ?? "unknown"}`);
  if (status.note) {
    line(`- Note: ${status.note}`);
  }
  line("");
}

function renderTrustSurfaces() {
  line("Trust surfaces");
  trustSurfaces.forEach((surface, index) => {
    line(
      `${index + 1}. ${surface.label} — ${surface.className}; machine enforced: ${surface.machineEnforced ? "yes" : "no"}`
    );
    line(`   Path: ${surface.path}`);
    line(`   Note: ${surface.note}`);
  });
  line("");
}

function renderNotClaimed() {
  line("What is not claimed");
  notClaimed.forEach((claim, index) => line(`${index + 1}. ${claim}`));
  line("");
}

function renderMenu() {
  line("What do you want to see?");
  menuOptions.forEach((option, index) => line(`${index + 1}. ${option}`));
  line("");
}

function renderSnapshot() {
  const status = readStatus();
  renderHeader();
  renderStatus(status);
  renderTrustSurfaces();
  renderNotClaimed();
  renderMenu();
}

function handleChoice(choice, rl) {
  switch (choice.trim().toLowerCase()) {
    case "1":
    case "status":
      renderStatus(readStatus());
      break;
    case "2":
    case "trust":
      renderTrustSurfaces();
      break;
    case "3":
    case "claims":
      renderNotClaimed();
      break;
    case "4":
    case "exit":
    case "quit":
      line("Exiting. Check the cited source files before promoting any claim.");
      rl.close();
      return;
    default:
      line("I did not understand that choice. Please enter 1, 2, 3, or 4.");
      line("");
  }

  renderMenu();
  rl.prompt();
}

function runInteractive() {
  renderSnapshot();

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: "Choose 1-4> ",
  });

  rl.prompt();
  rl.on("line", (input) => handleChoice(input, rl));
}

if (process.argv.includes("--help")) {
  line("Usage:");
  line("  npm run tui");
  line("  npm run tui -- --snapshot");
  process.exit(0);
}

if (process.argv.includes("--snapshot")) {
  renderSnapshot();
  process.exit(0);
}

runInteractive();
