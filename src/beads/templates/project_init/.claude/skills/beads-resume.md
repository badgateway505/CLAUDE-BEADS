# Resume Project

Restore project context and find the next action.

**Usage:** `/beads:resume`

**Why This Matters:** Resume restores the mental model without re-reading the entire project. Context loss between sessions is the #1 source of inconsistent work — wrong assumptions, repeated mistakes, or missed dependencies.

---

## Execution Protocol

### Step 1: Read Project State

Use the Read tool to read:
1. `.beads/ledger.json` — current state, completed beads, active bead
2. `.planning/PROJECT.md` — project vision, core function, tech stack

### Step 2: Show Project Overview

Present a concise summary:

```
Project : {name from PROJECT.md}
Core    : {core function — one sentence}
Stack   : {tech stack summary}

Roadmap:
  Phase 01: {name} — {Complete/In Progress/Pending}
  Phase 02: {name} — {Complete/In Progress/Pending}
  ...

Progress: {completed beads}/{total beads} beads, {completed phases}/{total phases} phases
```

### Step 3: Phase 01 Evaluation Status

If Phase 01 is closed, check `.planning/DECISIONS.md` for the evaluation outcome:
- **Continue** → note it was validated
- **Pivot** → note the adjusted direction
- **Kill** → note project was shelved
- **No evaluation recorded** → flag this: "Phase 01 was closed without evaluation. Consider running the evaluation before proceeding."

If Phase 01 is still in progress or pending, skip this step.

### Step 4: Identify Current State

Check what's active:

1. **`.beads/fsm-state.json` exists** → bead is mid-execution. Show the bead ID and current FSM state.
2. **Ledger has active bead** → bead is queued but not started. Show the bead ID.
3. **No active bead, phase has pending beads** → next bead needs to be initialized.
4. **No active bead, all beads complete** → phase is done, needs closing.
5. **No phases planned** → project needs `/beads:plan-project`.

### Step 5: Recommend Next Action

Based on current state, give ONE clear recommendation:

| State | Recommendation |
|-------|---------------|
| Bead mid-execution | "Continue with `/beads:run` — bead XX-YY is in progress" |
| Bead queued | "Run `/beads:run` to start bead XX-YY" |
| Phase beads all done | "Run `/beads:close-phase` to freeze Phase XX" |
| Phase closed, next planned | "Run `/beads:plan-phase XX` to decompose next phase" |
| No phases planned | "Run `/beads:plan-project` to create the roadmap" |
| Project complete | "All phases complete. Project is done." |

---

## Important Rules

- **DO NOT execute any FSM commands** — resume is read-only
- **DO NOT start beads** — just report state and recommend
- **DO read ledger.json and PROJECT.md** — these are the authoritative sources

---

**Related commands:**
- `/beads:run` — Execute the active bead
- `/beads:plan-phase` — Plan next phase if needed
- `/beads:plan-project` — Create project roadmap
