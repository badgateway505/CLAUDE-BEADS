# Onboard Existing Project

Analyze an existing codebase, detect issues, and prepare PROJECT.md for Beads planning.

**Usage:** `/beads:onboard`

**Why This Matters:** Onboarding captures what exists before planning what's next. Skipping this leads to duplicate work, missed constraints, or plans that conflict with existing architecture.

**What it does:**
This skill is for projects that already have code. It scans the codebase, gathers context from the user, and writes a rich PROJECT.md — without touching existing code or generating a roadmap. Roadmap generation is done separately via `/beads:plan-project`.

---

## Execution Protocol

### Step 1: Read Existing PROJECT.md

Read `.planning/PROJECT.md` first — it already has Vision and Goals from `beads init`.
Do NOT ask the user to repeat what they already provided.

Then ask only what's missing:

1. **What's the current state?** (working MVP? half-built? prototype? broken?)
2. **What are the immediate priorities?** (what should be built next?)

### Step 2: Lightweight Codebase Scan

Analyze the project structure — do NOT read every file. Token budget for scanning: keep it minimal.

**Do:**
- Read `README.md`, `pyproject.toml` / `package.json` / `Cargo.toml` (whatever exists)
- Run `tree` or glob for top-level structure
- Skim key entry points (main app file, config, routes)
- Check `git log --oneline -20` for recent activity
- Note the tech stack, dependencies, test coverage (exists or not)

**Do NOT:**
- Read every source file
- Read test files in detail
- Analyze implementation line-by-line
- Spend more than ~2K tokens on scanning

### Step 3: Detect Issues

Flag severe/high-risk issues found during scanning. Categorize as:

- **Severe**: Security risks, hardcoded secrets, broken dependencies
- **High**: Missing tests, no CI/CD, large monolithic files (800+ lines)
- **Info**: Missing .env.example, no README, outdated dependencies

Do NOT fix anything — only list observations.

### Step 4: Enrich PROJECT.md

**Do NOT overwrite** — the file already has Vision and Goals from `beads init`. Add new sections after the existing content, before the `## Phases` line.

Add these sections:

```markdown
## Current State
{what's already built — from user answer + scan findings}
- List major features/modules that exist and work
- List features that are partially built
- List what's completely missing

## Tech Stack
{detected from scan — language, framework, dependencies, infrastructure}

## Priorities
{from user answer — what should be built next}

## Observations
{issues detected during scan — categorized by severity}
- [SEVERE] "API key hardcoded in config.py line 42"
- [HIGH] "No test directory found — consider adding tests"
- [HIGH] "Large monolithic file (app.py, 800+ lines) — may benefit from splitting"
- [INFO] "No .env.example — API keys may not be documented"
```

The `## Current State` section is critical — `/beads:plan-project` uses it to know what's already done and only plan forward.

### Step 5: Report

Print a compact summary:

```
Onboarding complete

  Project : {name}
  Stack   : {detected stack}
  Issues  : {severe} severe, {high} high, {info} info

  Created: .planning/PROJECT.md

  Next steps:
  1. Review .planning/PROJECT.md — especially the Observations section
  2. Run /beads:plan-project to generate your phase roadmap
```

---

## Important Rules

- **NEVER modify existing source code.** Onboarding is read-only for the codebase.
- **NEVER create bead files.** Phase planning is done via `/beads:plan`.
- **NEVER generate a roadmap.** That's `/beads:plan-project`.
- **NEVER run tests or verification.** That happens during bead execution.
- **DO ask all questions before scanning.** User context is more valuable than code scanning.

---

**When to use:**
- After `beads init`, when the project already has code
- Project has existing code and PROJECT.md has only TODO placeholders
- Migrating from another workflow framework

**Related commands:**
- `/beads:plan-project` — Generate full phase roadmap (run after onboard + init)
- `/beads:plan phase-XX` — Decompose a specific phase into beads
- `/beads:resume` — Use instead of onboard if Beads is already set up with a real ledger
