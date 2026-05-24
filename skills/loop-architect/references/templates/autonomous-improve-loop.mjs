#!/usr/bin/env node
/**
 * Autonomous improvement controller scaffold.
 *
 * Use only after Loop Readiness is 6/6: signal, interpreter, change surface,
 * cadence, rollback, and owner are all defined. The controller turns one
 * failed trace/eval into one proposed diff, gates it, then leaves the result
 * for review instead of silently mutating production.
 */
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const CONFIG = {
  traceToEval: ["npm", "run", "trace:to-eval", "--", "--input", ".sdlc-harness/events.jsonl", "--out", "ai-ops/trace-eval-candidates/latest.json"],
  liveEval: ["npm", "run", "eval:ai", "--", "--live"],
  benchmark: ["npm", "run", "benchmark:system"],
  allowedChangeSurfaces: [
    "src/onboarding/chat.ts",
    "src/tui/agent/inline-probe.ts",
    "src/miner/probe-packs/",
    "CLAUDE.md",
    "AGENTS.md",
    ".cursor/rules/",
  ],
  proposedPatchPath: "ai-ops/proposed-improvement.patch",
};

function run([cmd, ...args]) {
  const res = spawnSync(cmd, args, { stdio: "inherit", shell: false });
  if (res.status !== 0) throw new Error(`command failed: ${cmd} ${args.join(" ")}`);
}

function writeProposedPatch() {
  mkdirSync(dirname(CONFIG.proposedPatchPath), { recursive: true });
  if (!existsSync(CONFIG.proposedPatchPath)) {
    writeFileSync(
      CONFIG.proposedPatchPath,
      [
        "# TODO: ask an optimizer model to write exactly one minimal diff.",
        "# Inputs: latest trace-eval candidate, failing eval output, allowedChangeSurfaces.",
        "# Constraint: patch only allowlisted files; prefer deleting stale rules over appending.",
        "",
      ].join("\n"),
    );
  }
  console.log(`Review or replace ${CONFIG.proposedPatchPath}; then apply it in a branch.`);
}

function main() {
  console.log("1/4 Promoting trace to eval candidate");
  run(CONFIG.traceToEval);
  console.log("2/4 Proposing one allowlisted improvement diff");
  writeProposedPatch();
  console.log("3/4 Run evals after applying the proposed diff in a branch");
  run(CONFIG.liveEval);
  console.log("4/4 Run benchmark and keep the diff only if all gates pass");
  run(CONFIG.benchmark);
}

main();
