# Close Current Phase

Freeze the current phase and prepare for the next one.

**Usage:** `/beads:close-phase`

**Why This Matters:** Phase closure freezes context and enables boundary guards. Without it, old bead context pollutes new work, state drifts between phases, and the FSM cannot enforce phase ordering.

---

## Execution Protocol

### Step 1: Identify Current Phase

Use the Read tool to read `.beads/ledger.json`. Find the current phase from the `beads` dict — the phase of the most recently completed bead.

### Step 2: Close Phase via FSM (MANDATORY)

```bash
python3 .beads/bin/fsm.py close-phase XX
```

Where `XX` is the current phase number (e.g. `01`).

If it fails with incomplete beads — STOP and tell the user which beads are still pending.

### Step 3: Create Phase Summary

Create `.planning/phases/XX-phase-name/XX-SUMMARY.md`:

```markdown
# Phase XX: [Phase Name] — SUMMARY

**Status:** CLOSED
**Closed:** [date]

## What Was Built

[2-4 sentences describing what was delivered]

## Key Decisions

- [Any important technical decisions made]

## Deliverables

- [x] Bead XX-01: [title] — [one-line outcome]
- [x] Bead XX-02: [title] — [one-line outcome]

## Context for Future Phases

[Anything the next phase needs to know: file paths, patterns, gotchas]
```

### Step 3b: Persist Key Decisions

If the phase produced any architectural or technical decisions (recorded in the "Key Decisions" section of the SUMMARY), append them to `.planning/DECISIONS.md`.

This ensures decisions survive phase closure. The SUMMARY gets `.claudeignore`d, but DECISIONS.md persists across all phases.

### Step 3c: Phase 01 Evaluation Gate

**Only for Phase 01.** For all other phases, skip to Step 4.

Phase 01 is the proof-of-concept. Before moving on, the user needs to decide whether the core idea validated. Present a structured evaluation:

1. **Summarize what was built** vs the core function defined in `.planning/PROJECT.md` (`## Core Function` section).

2. **Give your honest assessment:**
   > "Here's what Phase 01 proved:
   >
   > **What works:** [concrete strengths — what the prototype demonstrated]
   > **What concerns me:** [honest issues — gaps, limitations, things that felt harder than expected]
   >
   > **Does the core function work as you expected?**
   >
   > **1** — Continue — the idea validates, proceed to Phase 02
   > **2** — Pivot — the idea needs adjustment, re-plan before continuing
   > **3** — Kill — shelve the project, not worth pursuing further"

3. **Record the outcome** in `.planning/DECISIONS.md`:
   ```markdown
   | Phase 01 evaluation: [Continue/Pivot/Kill] | [one-line rationale from user] | 01 | — |
   ```

4. **If Pivot:** Tell the user to update `.planning/PROJECT.md` with the adjusted direction, then re-run `/beads:plan-project` to re-plan the roadmap.

5. **If Kill:** Print "Project shelved after Phase 01 evaluation." and stop. Do not proceed to Step 4.

### Step 4: Update .claudeignore

Add the phase's detailed files to `.claudeignore` so they don't pollute future context. Only the SUMMARY.md stays readable.

Append to `.claudeignore`:
```
# Phase XX frozen — read XX-SUMMARY.md instead
.planning/phases/XX-phase-name/beads/
```

### Step 5: Report

```
Phase XX closed

  Beads completed : N
  Summary         : .planning/phases/XX-phase-name/XX-SUMMARY.md

  Next: Run `/beads:plan-phase XX+1` to plan the next phase
```

---

## Important Rules

- **NEVER skip `fsm.py close-phase`** — it marks the phase closed in ledger, enabling the phase boundary guard
- **NEVER proceed to next phase without this** — `fsm.py check-phase-closed` will block `/beads:plan-phase`
- **DO create SUMMARY.md** — it's the only context kept for closed phases

---

**Related commands:**
- `/beads:plan-phase` — Plan the next phase after closing
- `/beads:run` — If beads are still pending before closing
