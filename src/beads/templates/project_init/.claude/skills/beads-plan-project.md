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

Use the output from this command as your source data — do NOT re-read PROJECT.md separately.

### Step 1: Read Additional Context

Read these files for extra context:

1. `.planning/PROJECT.md` — full project doc (may have `## Current State` from `/beads:onboard`)
2. `.beads/ledger.json` — current state
3. `CLAUDE.md` — any existing project context

**Key check:** Does PROJECT.md have a `## Current State` section?
- **YES** → This is an existing project. The Current State section lists what's already built. Only plan phases for remaining work.
- **NO** → This is a new project. Plan everything from scratch.

Infer the best tech stack from the project description and goals (or use `## Tech Stack` if onboard already detected it). Include your stack recommendation in the phase plan for user confirmation.

### Step 2: Generate Phase Roadmap

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

### Step 3: Confirm with User

Present the roadmap and ask:
- Does this look right?
- Any phases missing or out of order?
- Any phases that should be split or merged?

Wait for approval before writing.

### Step 4: Create Phase Directories

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

### Step 5: Update Ledger

Update `.beads/ledger.json` with:
- **Project Vision** (from PROJECT.md)
- **Global Context** (stack, constraints from PROJECT.md)
- **Roadmap Overview** table with all phases (Complete phases marked `✅`, first pending marked `🔄 Active`)
- Active Bead: **None** — Run `/beads:plan phase-{first_pending}` to decompose first pending phase

Use FSM sync-ledger if available:
```bash
python3 .beads/bin/fsm.py sync-ledger
```

### Step 6: Cleanup and Report

Remove the plan-ready flag (one-time use):
```bash
rm -f .beads/.plan-ready
```

Print summary:
```
Roadmap complete

  Project : {name}
  Phases  : {complete} complete, {pending} pending
  Next    : Phase {first_pending} — {name}

  Next steps:
  1. Review phase overviews in .planning/phases/
  2. Run /beads:plan phase-{first_pending} to decompose into beads
  3. Run /beads:run to execute first bead
```

---

## Important Rules

- **NEVER create bead files.** Phase decomposition into beads is done via `/beads:plan phase-XX`.
- **NEVER modify existing source code.** This is a planning-only skill.
- **NEVER skip user confirmation.** Always present the roadmap for approval before writing files.
- **DO update PROJECT.md** if the user provides new context during this session.
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
