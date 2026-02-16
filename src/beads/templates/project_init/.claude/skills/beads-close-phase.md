# Close Current Phase

Freeze the current phase and prepare for the next one.

**Usage:** `/beads:close-phase`

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
