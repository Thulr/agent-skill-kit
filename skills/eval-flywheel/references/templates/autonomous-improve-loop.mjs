#!/usr/bin/env node
/**
 * Autonomous improvement controller.
 *
 * Turns one failed trace/eval into one allowlisted patch, gates it, and keeps
 * it only if the eval/benchmark commands pass. Default mode writes a patch for
 * review. Run with `--apply` to apply in a branch, gate, and stage on success.
 */
import {
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { dirname, join } from "node:path";
import { spawnSync } from "node:child_process";

const CONFIG = {
  model: process.env.OPTIMIZER_MODEL || "gpt-5",
  candidatePath:
    process.env.TRACE_EVAL_CANDIDATE || "ai-ops/trace-eval-candidates/latest.json",
  patchPath: process.env.PROPOSED_PATCH || "ai-ops/proposed-improvement.patch",
  reportPath: process.env.IMPROVE_REPORT || "ai-ops/improve-loop-report.json",
  traceToEval: cmd(process.env.TRACE_TO_EVAL_CMD) || [
    "npm",
    "run",
    "trace:to-eval",
    "--",
    "--input",
    ".sdlc-harness/events.jsonl",
    "--out",
    "ai-ops/trace-eval-candidates/latest.json",
  ],
  liveEval: cmd(process.env.LIVE_EVAL_CMD) || [
    "npm",
    "run",
    "eval:ai",
    "--",
    "--live",
  ],
  heldOutEval: cmd(process.env.HELD_OUT_EVAL_CMD),
  benchmark: cmd(process.env.BENCHMARK_CMD) || ["npm", "run", "benchmark:system"],
  allowlist: (
    process.env.ALLOWED_CHANGE_SURFACES ||
    "src/onboarding/chat.ts,src/tui/agent/inline-probe.ts,src/miner/probe-packs/,CLAUDE.md,AGENTS.md,.cursor/rules/"
  )
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean),
  maxFileBytes: Number(process.env.MAX_OPTIMIZER_FILE_BYTES || 20000),
};

const DOCTRINE = `
Use the self-improving-system loop: signal -> interpretation -> durable change
-> next run. Tests/evals are the verifier, not the actuator. Prefer durable
artifacts: eval cases, prompt/rule diffs, tool schemas, tests, harness checks,
or deleted stale scaffolding. Make one minimal change. Preserve train/held-out
separation. Do not optimize a visible score by weakening the real task. Redact
secrets, avoid prompt bloat, and prefer merging/deleting stale rules over
appending. Output a unified diff only.
`.trim();

const args = new Set(process.argv.slice(2));
const applyPatch = args.has("--apply");
const skipTrace = args.has("--skip-trace");
const allowDirty = args.has("--allow-dirty");
const branchName =
  valueAfter("--branch") ||
  process.env.IMPROVE_BRANCH ||
  `ai-improve/${new Date().toISOString().replace(/[:.]/g, "-")}`;

function cmd(value) {
  if (!value) return null;
  return value.split(" ").filter(Boolean);
}

function valueAfter(flag) {
  const index = process.argv.indexOf(flag);
  return index === -1 ? null : process.argv[index + 1];
}

function run(command, options = {}) {
  const [bin, ...argv] = command;
  const res = spawnSync(bin, argv, {
    stdio: options.capture ? "pipe" : "inherit",
    encoding: "utf8",
  });
  if (options.allowFailure) return res;
  if (res.status !== 0) throw new Error(`command failed: ${command.join(" ")}`);
  return res;
}

function git(args, options) {
  return run(["git", ...args], options);
}

function ensureCleanTree() {
  const status = git(["status", "--porcelain"], { capture: true }).stdout.trim();
  if (status && !allowDirty) {
    throw new Error("worktree is dirty; commit/stash or rerun with --allow-dirty");
  }
}

function redact(text) {
  return text
    .replace(/sk-[A-Za-z0-9_-]{20,}/g, "sk-REDACTED")
    .replace(/(api[_-]?key|token|secret|password)["'=:\s]+[^"'\s,}]+/gi, "$1=REDACTED");
}

function collectFiles() {
  const files = [];
  for (const surface of CONFIG.allowlist) collectSurface(surface, files);
  return files;
}

function collectSurface(surface, files) {
  if (!existsSync(surface)) return;
  const info = statSync(surface);
  if (info.isFile()) return pushFile(surface, files);
  if (!info.isDirectory()) return;
  for (const entry of readdirSync(surface)) {
    if (entry === "node_modules" || entry === ".git") continue;
    collectSurface(join(surface, entry), files);
  }
}

function pushFile(path, files) {
  const bytes = statSync(path).size;
  if (bytes > CONFIG.maxFileBytes) return;
  files.push({
    path,
    content: redact(readFileSync(path, "utf8")),
  });
}

async function callOptimizer(candidate, files) {
  if (!process.env.OPENAI_API_KEY) {
    throw new Error("OPENAI_API_KEY is required to generate an improvement patch");
  }
  const body = {
    model: CONFIG.model,
    instructions: DOCTRINE,
    input: [
      "Failed trace/eval candidate:",
      redact(candidate),
      "",
      "Allowlisted change surfaces and file contents:",
      JSON.stringify(files, null, 2),
      "",
      `Allowed paths: ${CONFIG.allowlist.join(", ")}`,
      "Return only a unified diff touching those paths.",
    ].join("\n"),
    store: false,
  };
  const res = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`optimizer failed: ${res.status} ${await res.text()}`);
  return extractText(await res.json());
}

function extractText(response) {
  if (response.output_text) return response.output_text;
  const chunks = [];
  for (const item of response.output || []) {
    for (const part of item.content || []) {
      if (part.text) chunks.push(part.text);
    }
  }
  return chunks.join("\n");
}

function extractDiff(text) {
  const match = text.match(/```(?:diff|patch)?\n([\s\S]*?)```/);
  return (match ? match[1] : text).trim() + "\n";
}

function looksSubstantive(value) {
  if (!value) return false;
  if (typeof value === "string") return value.length >= 50;
  if (Array.isArray(value)) return value.length > 0;
  if (typeof value === "object") return Object.keys(value).length > 0;
  return false;
}

function preflight(candidateText) {
  // The autonomous improvement loop is only useful when (a) the trace
  // candidate actually carries LLM I/O the optimizer can learn from, and
  // (b) there is a held-out eval to gate against fixture contamination.
  // Without either, the controller produces skeleton diffs that pass
  // training and fail in production. See SKILL.md "Telemetry Theater".
  const issues = [];
  let parsed;
  try {
    parsed = JSON.parse(candidateText);
  } catch {
    parsed = null;
  }
  const hasLlmIo =
    parsed &&
    (looksSubstantive(parsed.prompt) ||
      looksSubstantive(parsed.completion) ||
      looksSubstantive(parsed.tool_io) ||
      looksSubstantive(parsed.messages) ||
      looksSubstantive(parsed.response));
  if (!hasLlmIo) {
    issues.push(
      "candidate has no prompt/completion/tool_io content — refusing to optimize from metadata-only trace. " +
        "Wrap your LLM client calls so prompts and completions land in the span/event log " +
        "(see SKILL.md 'Telemetry Theater'). Set TRACE_EVAL_CANDIDATE to a richer candidate if one exists.",
    );
  }
  if (!CONFIG.heldOutEval) {
    issues.push(
      "HELD_OUT_EVAL_CMD is unset — no train/test separation. " +
        "Set HELD_OUT_EVAL_CMD to a command that runs evals the optimizer never sees, " +
        "or the controller will overfit to its training fixtures.",
    );
  }
  if (issues.length) {
    console.error("preflight failed:\n  - " + issues.join("\n  - "));
    process.exit(2);
  }
}

function changedPaths(diff) {
  const paths = new Set();
  for (const line of diff.split("\n")) {
    const m = line.match(/^diff --git a\/(.+?) b\/(.+)$/);
    if (m) {
      paths.add(m[1]);
      paths.add(m[2]);
    }
    const p = line.match(/^(?:---|\+\+\+) (?:a|b)\/(.+)$/);
    if (p) paths.add(p[1]);
  }
  return [...paths].filter((p) => p !== "/dev/null");
}

function assertAllowlisted(diff) {
  const paths = changedPaths(diff);
  if (paths.length === 0) throw new Error("optimizer returned no changed paths");
  for (const path of paths) {
    if (path.startsWith("/") || path.includes("..")) {
      throw new Error(`unsafe patch path: ${path}`);
    }
    if (!CONFIG.allowlist.some((allowed) => path === allowed || path.startsWith(allowed))) {
      throw new Error(`patch touches non-allowlisted path: ${path}`);
    }
  }
  return paths;
}

function writeReport(report) {
  mkdirSync(dirname(CONFIG.reportPath), { recursive: true });
  writeFileSync(CONFIG.reportPath, JSON.stringify(report, null, 2) + "\n");
}

async function main() {
  ensureCleanTree();
  if (!skipTrace) run(CONFIG.traceToEval);
  if (!existsSync(CONFIG.candidatePath)) {
    throw new Error(`missing trace/eval candidate: ${CONFIG.candidatePath}`);
  }

  const candidate = readFileSync(CONFIG.candidatePath, "utf8");
  preflight(candidate);
  const files = collectFiles();
  const patch = extractDiff(await callOptimizer(candidate, files));
  const paths = assertAllowlisted(patch);
  mkdirSync(dirname(CONFIG.patchPath), { recursive: true });
  writeFileSync(CONFIG.patchPath, patch);
  git(["apply", "--check", CONFIG.patchPath]);

  if (!applyPatch) {
    writeReport({ status: "patch_proposed", patchPath: CONFIG.patchPath, paths });
    console.log(`Patch proposed at ${CONFIG.patchPath}. Re-run with --apply to gate it.`);
    return;
  }

  git(["switch", "-c", branchName]);
  git(["apply", CONFIG.patchPath]);
  const gates = [CONFIG.liveEval, CONFIG.heldOutEval, CONFIG.benchmark].filter(Boolean);
  const failed = gates.find((gate) => run(gate, { allowFailure: true }).status !== 0);
  if (failed) {
    git(["apply", "-R", CONFIG.patchPath], { allowFailure: true });
    writeReport({ status: "reverted", failedGate: failed.join(" "), patchPath: CONFIG.patchPath });
    throw new Error(`gate failed; patch reverted: ${failed.join(" ")}`);
  }

  git(["add", ...paths.filter((p) => existsSync(p) || existsSync(dirname(p)))]);
  writeReport({ status: "staged", branch: branchName, patchPath: CONFIG.patchPath, paths });
  console.log(`Improvement staged on ${branchName}. Review, commit, and open a PR.`);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
