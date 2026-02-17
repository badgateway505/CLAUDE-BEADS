# Run Active Bead

Execute the currently active bead — your atomic unit of real, verified work.

**Usage:** `/beads:run`

**Tip:** Run `/clear` before each bead for optimal token efficiency.

---

## Why This Process Matters

Each bead is a small, focused task with clear success criteria. The FSM tracks your progress, preserves your audit trail, and queues the next task automatically. Working through the FSM means your work is properly recorded — every completed bead is proof of real progress.

---

## Execution Flow

### Step 1: Find Your Active Bead

Check for the active bead using the Read tool:

1. **Check `.beads/fsm-state.json` first** — if it exists with `current_state: "execute"`, you're already initialized. The `bead_path` field points to your bead file.
2. **Otherwise check `.beads/ledger.json`** → `active_bead` field for the bead ID, then find its file in `.planning/phases/`.
3. **If no active bead exists**, let the user know:
   > "No active bead. Run `/beads:plan-phase XX` to create and initialize beads."

### Step 2: Understand the Bead

Read the bead `.md` file. Understand:
- What needs to be accomplished (tasks, acceptance criteria)
- How success is measured (verification tier and command)
- What context you need (files listed in `<context_files>`)
- Preferred model for this work (opus / sonnet / haiku)

Read all `<context_files>` before starting — good context leads to good work.

### Step 3: Initialize via FSM

If `fsm-state.json` already shows `execute` state for this bead, you're ready — proceed.

Otherwise, initialize through the FSM so your work is tracked:
```bash
python3 .beads/bin/fsm.py init <bead-id> --bead <path>
```

If the FSM raises an error (phase boundary, missing dependency), surface it to the user with full context. These checks exist to catch real problems — a blocked init means something needs the user's attention first.

### Step 4: Challenge Your Approach (Zero Trust)

Before writing code, state your planned approach and find at least one concrete way it could fail — a wrong assumption, an edge case, a better alternative. If the risk is valid, adjust. If the approach is genuinely straightforward, say why in one sentence.

This is not a ritual. It prevents the most common failure mode: committing to the first idea that "feels right" without stress-testing it.

### Step 5: Execute Tasks

Work through each task in the bead sequentially. The bead was designed as a coherent unit — follow the task descriptions to deliver exactly what's specified.

### Step 6: Prove Your Work

Verification is your evidence that the code actually works. Run the real verification command through the FSM:

**AUTO tier** — run the actual test suite:
```bash
python3 .beads/bin/fsm.py verify "<verification_cmd>"
```
A real test pass means the code is solid. This is the most valuable part of the process — it turns "I think it works" into "I proved it works."

**MANUAL tier** — walk through each checklist item with the user, then confirm:
```bash
python3 .beads/bin/fsm.py verify "echo manual-checklist-passed"
```

**NONE tier (spikes)** — confirm the finding document exists, then:
```bash
python3 .beads/bin/fsm.py verify "echo spike-complete"
```

### Step 7: Report

Summarize what you delivered:

---

## ✅ Bead XX-YY — [title]

| | |
|---|---|
| 🔍 Verify | PASS |
| 🔨 Commit | `sha` |

**Files delivered:**
- `path/to/file` — one-line description

---

> **Next:** `/beads:run` for bead XX-YY+1
> or `/beads:close-phase` if this was the last bead in the phase

---

## Working Well Together

- **FSM is your ally.** It tracks progress, syncs the ledger, and queues next work automatically. All state changes flow through it — this keeps your audit trail clean and your work properly credited.
- **Verification is your proof.** Running the real test command is what separates done-for-real from done-on-paper. Take pride in a genuine pass.
- **Errors are information.** If the FSM blocks you, it caught something real. Surface it to the user with context so you can solve it together.
- **On failure, diagnose before retrying.** State what went wrong and why before attempting a fix. Blind retries waste tokens and repeat mistakes. A different approach beats a tweaked version of the same one.

---

**Related:** `/beads:plan-phase`, `/beads:resume`, `/beads:close-phase`
