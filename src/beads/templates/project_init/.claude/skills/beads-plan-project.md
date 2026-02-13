# Plan Project Roadmap

Generate a full phase roadmap for the entire project based on PROJECT.md.

**Usage:** `/beads:plan-project`

**What it does:**
This skill reads `.planning/PROJECT.md` and creates a complete phase roadmap — from current state to the end goal. It does NOT decompose phases into beads (that's `/beads:plan phase-XX`).

---

## Execution Protocol

### Step 0: Validate Project (MANDATORY)

Run this FIRST — the hook will block all phase writes without it:

```bash
python3 .beads/bin/fsm.py validate-project
```

This validates PROJECT.md has real content and unlocks `.planning/phases/` for writing.
If it fails, fix PROJECT.md before proceeding.

### Step 1: Read Context

Use the **Read tool** (not bash cat) to read these files:
1. `.planning/PROJECT.md` — vision and goals from `beads init`
2. `.beads/ledger.json` — current state
3. `CLAUDE.md` — any existing project context

**Key check:** Does PROJECT.md have a `## Current State` section?
- **YES** → Existing project. Only plan phases for remaining work.
- **NO** → New project. Plan everything from scratch.

### Step 2: Guided Dialogue

Go one topic at a time. For each, propose a sensible default based on the vision, present quick-reply options, and wait for the user's response before moving on.

**1. Goals**
Propose 3-5 specific goals inferred from the vision:
> "Based on your description, here are the goals I'd suggest:
> 1. [goal]
> 2. [goal]
> 3. [goal]
>
> Reply with:
> **1** — Looks good, continue
> **2** — Adjust (tell me what to change)"

Wait for reply, then move to next topic.

**2. Success criteria**
Propose what "done" looks like based on the confirmed goals:
> "Here's how I'd define 'done':
> - [criterion]
> - [criterion]
>
> Reply with:
> **1** — Correct, continue
> **2** — Adjust (tell me what to change)"

Wait for reply, then move to next topic.

**3. Constraints**
> "Any technical or timeline constraints?
> (e.g. must use Python 3.11+, deploy by X date, no paid dependencies)
>
> Reply with:
> **1** — None, continue
> **2** — Yes: [describe them]"

Wait for reply, then move to next topic.

**4. Tech stack**
Recommend the best stack for the project type, taking constraints into account. Be specific:
> "For a project like this, I'd recommend:
> - [tool/library] for [purpose]
> - [tool/library] for [purpose]
>
> Reply with:
> **1** — Works for me, continue
> **2** — Use a different stack: [describe]"

Wait for confirmation, then proceed to Step 3.

### Step 3: Generate Phase Roadmap

Create the phase roadmap. This is a high-level plan — phase titles and one-line goals only.

**For existing projects (has `## Current State`):**
- Mark already-built features as `Complete` phases
- Only create `Pending` phases for remaining work toward the end goal
- If observations/tech-debt were flagged, optionally include a cleanup phase (ask user)
- Phase numbering continues from where the project is (e.g., if 3 things are done, first new phase is 04)

**For new projects (no `## Current State`):**
- Plan everything from start to finish

**Rules (both cases):**
- Each phase should be 3-10 beads worth of work (roughly 1-3 days)
- Order by dependency — foundational work first, polish last
- Be specific to this project — no generic "Setup" or "Testing" phases unless they genuinely apply
- Include infrastructure, testing, and deployment phases if they're part of the end goal

**Phase format:**
```
Phase XX: [Name]
Goal: [One clear sentence — what this phase delivers]
Status: ✅ Complete | ⏳ Pending
```

### Step 4: Confirm with User

Present the roadmap and ask:
> "Does this look right? Any phases missing, out of order, or that should be split/merged?
>
> **1** — Looks good, create the phases
> **2** — Adjust: [describe changes]"

Wait for approval before writing.

### Step 5: Create Phase Directories

For each phase, create:
```
.planning/phases/XX-phase-name/
  XX-OVERVIEW.md
```

Each OVERVIEW.md contains:
```markdown
# Phase XX: [Name]

## Goal
[One sentence from roadmap]

## Deliverables
- [TODO — filled during /beads:plan phase-XX]

## Dependencies
- [Previous phase if applicable]

## Status
Pending
```

### Step 6: Update PROJECT.md

Update `.planning/PROJECT.md` with the confirmed info from the dialogue:
- Fill in `## Goals / MVP Target` with the confirmed goals
- Add `## Tech Stack` section with the confirmed stack
- Add `## Constraints` section if any were specified
- Add `## Success Criteria` section

Use the Write tool to update the file. This is the source of truth for planning.

### Step 7: Cleanup and Report

Remove the plan-ready flag (one-time use):
```bash
rm -f .beads/.plan-ready
```

Print summary using this exact format (wrap commands in backticks so they stand out):
```
Roadmap complete

  Project : {name}
  Phases  : {complete} complete, {pending} pending
  Next    : Phase {first_pending} — {name}

  Next steps:
  1. Run `/beads:plan phase-{first_pending}` to decompose into beads
  2. Then run `/beads:run` to execute the first bead
```

---

## Important Rules

- **NEVER create bead files.** Phase decomposition into beads is done via `/beads:plan phase-XX`.
- **NEVER modify existing source code.** This is a planning-only skill.
- **NEVER skip user confirmation.** Always present the roadmap for approval before writing files.
- **NEVER call `fsm.py sync-ledger` here** — the FSM has no active bead at this stage. The ledger is populated when you run `/beads:plan phase-XX`.
- **DO update PROJECT.md** with all confirmed context from the dialogue.
- **DO mark already-completed work** as `Complete` if the project has existing code (check git log).

---

**When to use:**
- After `beads init` for new projects — to create the full phase plan
- When starting fresh and PROJECT.md has TODO placeholders
- When you want to re-plan the entire project roadmap

**Related commands:**
- `/beads:plan phase-XX` — Decompose a specific phase into atomic beads (run after this)
- `/beads:onboard` — For existing projects, scan codebase and analyze before planning
- `/beads:run` — Execute beads after planning
