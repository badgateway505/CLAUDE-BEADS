# Run Active Bead

Execute the currently active bead.

**Usage:** `/beads:run`

**Tip:** Run `/clear` before each bead for optimal token efficiency (not enforced).

---

## Execution Protocol

### Step 1: Find Active Bead

Use the **Read tool** (not bash) to check for the active bead:

1. **First check `.beads/fsm-state.json`** — if it exists with `current_state: "execute"`, the bead is already initialized. Read the `bead_path` field to find the bead file.
2. **If no fsm-state.json**, check `.beads/ledger.json` → `active_bead` field for the bead ID, then find its file in `.planning/phases/`.
3. **If no active bead found**, tell the user:
   > "No active bead. Run `/beads:plan-phase XX` to create and initialize beads."

### Step 2: Read Bead File

Use the **Read tool** to read the bead `.md` file. Extract:
- Task description, acceptance criteria, context files
- Verification tier (AUTO / MANUAL / NONE) and verification command
- Model (opus / sonnet / haiku)

Read all files listed in `<context_files>` before starting work.

### Step 3: Verify FSM State

If `fsm-state.json` already shows `execute` state for this bead, proceed directly.

If NOT initialized, run:
```bash
python3 .beads/bin/fsm.py init <bead-id> --active-model <model> --bead <path>
```

### Step 4: Execute Tasks

Execute each task in the bead sequentially. Follow the task descriptions exactly.

### Step 5: Verify

Run the bead's verification through the FSM:

**AUTO tier:**
```bash
python3 .beads/bin/fsm.py verify "<verification_cmd>"
```

**MANUAL tier:**
Go through each checklist item with the user, then:
```bash
python3 .beads/bin/fsm.py verify "echo manual-checklist-passed"
```

**NONE tier (spikes):**
Confirm the deliverable exists, then:
```bash
python3 .beads/bin/fsm.py verify "echo spike-complete"
```

### Step 6: Report

```
Bead XX-YY complete

  Task   : [title]
  Verify : PASS
  Commit : [sha]

  Next: `/beads:run` for the next bead
        or `/beads:close-phase` if all phase beads are done
```

---

## Important Rules

- **If FSM blocks you: STOP.** Show the user the error. Do not bypass.
- **Do NOT write to `.beads/ledger.json` directly** — the FSM manages it.
- **Do NOT skip verification** — the FSM won't complete without it.
- **Check `fsm-state.json` first** — it's the runtime source of truth for the active bead.

---

**Related:** `/beads:plan-phase`, `/beads:resume`, `/beads:close-phase`
